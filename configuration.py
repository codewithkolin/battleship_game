from configparser import ConfigParser, MissingSectionHeaderError
from exceptions import ConfigurationException
from errors import ErrorMessageCode
import json
from json.decoder import JSONDecodeError
from typing import Tuple, List
import string


DEFAULT_SIZE = 10
FLEETS = ["battleship", "cruiser", "destroyer", "submarine"]
FLEET_PROPERTIES = ["size", "quantity"]
DEFAULT_FLEET = {
    "battleship": {"size": 4, "quantity": 1},
    "cruiser": {"size": 3, "quantity": 2},
    "destroyer": {"size": 2, "quantity": 3},
    "submarine": {"size": 1, "quantity": 4},
}


def read_file(file_name: str) -> str:
    """
    Opens file, reads it and returns file content

    Args:
        file_name (str): file name to open

    Returns:
        str: file contents
    """

    try:
        with open(file_name) as config_file:
            data = config_file.read()
            return data
    except OSError:
        raise ConfigurationException(ErrorMessageCode.OSERROR.format(file_name))


class GameConfiguration(object):
    def __init__(self, board_size: int, config_file_name: str, option: bool):
        """Reads game configuration from config file

        Args:
            config_file_name (str): config file name
        """
        super().__init__()
        # global DEFAULT_SIZE
        # DEFAULT_SIZE = board_size
        self._size = DEFAULT_SIZE
        self._fleet = DEFAULT_FLEET
        self.config_file_name = config_file_name
        size_change = {}
        size_change["board"] = {"size": board_size}
        size_change['boat'] = DEFAULT_FLEET
        json_object = json.dumps(size_change, indent=2)
        with open("game_config.json", "w") as outfile:
            outfile.write(json_object)
        if option:
            self.interactive_board_setup(config_file_name)

    def interactive_board_setup(self, config_file_name):
        game_config = {}
        print("Please select size of Board.")
        print("Enter 1 for default 10x10")
        print("Enter 2 for custom board of X x X")
        board_size_opt = int(input("Please enter option now.\n"))
        if board_size_opt == 1:
            self._size = DEFAULT_SIZE
            print("Default Board of 10 x 10 size selected.\n")
        elif board_size_opt == 2:
            self._size = int(input("Please enter Board Size.\n"))
            if self._size > 26:
                print("Board size cannot exceed 26.")
                self._size = DEFAULT_SIZE
            print("Board size is " + str(self._size) + ' X ' + str(self._size))
        else:
            print("Incorrect option! Continuing with default Board of 10 X 10 size.\n")
            self._size = DEFAULT_SIZE
        game_config["board"] = {"size": self._size}
        print("Please select Type of Fleets.")
        print("Enter 1 for default Fleets.")
        print("Enter 2 for custom Fleets with size and quantity.")

        Fleet_size_opt = int(input("Please enter your option now.\n"))
        config = {}
        if Fleet_size_opt == 1:
            self._fleet = DEFAULT_FLEET
            for key, val in DEFAULT_FLEET.items():
                print(key, val)
            config['boat'] = DEFAULT_FLEET
            game_config.update(config)

        if Fleet_size_opt == 2:
            NEW_FLEET = {}
            Fleet_no = int(input("How many fleet you want to add?\n"))
            for i in range(Fleet_no):
                Fleet_name = str(input("Please enter fleet name.\n"))
                Fleet_size = int(input("Please enter fleet size.\n"))
                Fleet_quantity = int(input("Please enter fleet quantity.\n"))
                NEW_FLEET[Fleet_name] = {"size": Fleet_size, "quantity": Fleet_quantity}
                print(NEW_FLEET)
            self._fleet = NEW_FLEET
            config['boat'] = NEW_FLEET
            game_config.update(config)
        json_object = json.dumps(game_config, indent=2)

        # Writing to sample.json
        with open("game_config.json", "w") as outfile:
            outfile.write(json_object)
        self.config_file_name = config_file_name

    def fleet_position(self, config, player):
        dic = {}
        place = []
        print("To place you ship horizontal eg :- C5-H5 for horizontal placing ship")
        print("To place you ship vertical eg :- A1-A8 for vertical placing ship")
        for i, v in config.items():
            print("For fleet {} Please enter {} times.".format(i, v["quantity"]))
            for x in range(config[i]['quantity']):
                loc_input = str(input(
                    "Enter location to place your ship for fleet {} with size {}.\n".format(i, config[i]['size'])))
                place.append(loc_input)
            dic[i] = place
            place = []
            print(dic)

        json_object = json.dumps(dic, indent=2)

        # Writing to sample.json
        with open(player.lower() + "_board.json", "w") as outfile:
            outfile.write(json_object)
        return player.lower() + "_board.json"

    def _validate_boat_configuration(self, boat_name: str, values: dict):
        """
        validate boat values for game configuration
        each boat must has values for size and quantity

        Args:
            boat_name (str): boat type name
            values (dict): size and quantity configuration for each boat type

        Raises:
            ConfigurationException: if there was invalid boat_type or invalid value
        """
        if not values:
            raise ConfigurationException(ErrorMessageCode.INVALID_FLEET_CONFIGURATION)
        for value_key in values:
            if value_key not in FLEET_PROPERTIES:
                raise ConfigurationException(
                    ErrorMessageCode.INVALID_FLEET_CONFIGURATION
                )
            try:
                # validate value
                value = int(values[value_key])
                values[value_key] = value
            except ValueError:
                raise ConfigurationException(
                    ErrorMessageCode.INVALID_FLEET_CONFIGURATION
                )

            if value <= 0 or value > self._size:
                raise ConfigurationException(
                    ErrorMessageCode.INVALID_FLEET_CONFIGURATION
                )

    def load_configuration(self):
        """
        Reads json configuration file and parse board and boat type configuration
        This method defines board size and size-quantity for each boat type

        Raises:
            ConfigurationException: if configuration file or data was invalid
        """
        # read config file
        data = read_file(self.config_file_name)
        try:
            json_data = json.loads(data)
        except JSONDecodeError:
            # raise error if config file is invalid
            raise ConfigurationException(
                ErrorMessageCode.INVALID_CONFIGURATION.format(self.config_file_name)
            )
        # set board size
        self._size = json_data.get("board", {}).get("size", DEFAULT_SIZE)
        if self._size > 26:
            raise ConfigurationException(ErrorMessageCode.INVALID_BOARD_SIZE)
        if json_data.get("board"):
            # set fleet information
            self._fleet = {}
            for boat in json_data["boat"]:
                # get each ship name and its property
                values = json_data["boat"][boat]
                self._validate_boat_configuration(boat, values)
                self._fleet.setdefault(boat.lower(), values)

    @property
    def size(self) -> int:
        """Gets board size

        Returns:
            int: board size
        """
        return self._size

    @property
    def fleet(self) -> dict:
        """Get fleet information

        Returns:
            dict: each fleat's size and quantity
        """
        return self._fleet


class AddressingConfiguration(object):
    def __init__(self, board_size: int):
        super().__init__()
        self.board_size = board_size

    def _get_position_on_board(
        self, cell_name: str, error_message: str
    ) -> Tuple[int, int]:
        """
        Find cell position on board by cell name

        Args:
            cell_name (str): cell name e.g. A3
            error_message (str): if during validation an exception raised,
            this message will return as exception message

        Return:
            Tuple(int, int): indicates that cell name on board

        Raises:
            ConfigurationException: if cell name was invalid on the board
        """

        if len(cell_name) < 2 or len(cell_name) > 3:
            # just 2 letter referring is valid
            raise ConfigurationException(error_message)
        # for example A3
        col, row = cell_name[0], cell_name[1:]
        try:
            row = int(row)
        except ValueError:
            raise ConfigurationException(error_message)
        if row <= 0 or row > 26 or row > self.board_size:
            # maximum board size is 26
            raise ConfigurationException(error_message)
        row -= 1
        col_names = string.ascii_uppercase[: self.board_size]
        col = col_names.find(col.upper())
        if col == -1:
            # invalid column name
            raise ConfigurationException(error_message)
        return col, row

    def get_shots_positions(self, shots: List[str]) -> List[Tuple[int, int]]:
        """
        Recieves list of the player shots and return their position on the grid

        Args:
            shots (str): list of the shots e.g. ['A3', 'B5', 'C9' , ... ]

        Raises:
            ConfigurationException: if cell name was invalid on the board
        """
        positions = []
        for shot in shots:
            positions.append(
                self._get_position_on_board(
                    shot,
                    ErrorMessageCode.PLAYER_CONFIGURATION_INVALID_CELL_NAME.format(
                        shot
                    ),
                )
            )
        return positions


class PlayerBoardConfiguration(AddressingConfiguration):
    def __init__(
        self,
        player_label: str,
        config_file_name: str,
        board_size: int,
        fleet_configuration: dict,
    ):
        """Reads player fleet position configuration from json file

        Args:
            config_file_name (str): config file name
            board_size (int): board size
            fleet_configuration (dict): fleet configuration information from game's configuration
        """
        super().__init__(board_size=board_size)
        self.player_label = player_label
        self.fleet_configuration = fleet_configuration
        self.config_file_name = config_file_name
        self.fleet_positions = {}

    def _get_error_message(self, error_message: str) -> str:
        """
        Returns an error message with the player name
        """
        return f"{self.player_label} >>> {error_message}"

    def _get_position_on_board(self, cell_name: str) -> Tuple[int, int]:
        """
        Find cell position on board by cell name

        Args:
            cell_name (str): cell name e.g. A3

        Return:
            Tuple(int, int): indicates that cell name on board

        Raises:
            ConfigurationException: if cell name was invalid on the board
        """

        return super()._get_position_on_board(
            cell_name,
            ErrorMessageCode.PLAYER_CONFIGURATION_INVALID_CELL_NAME.format(
                self._get_error_message(cell_name)
            ),
        )

    def _get_boats_positions(
        self, cell_names: List[str], boat_size: int
    ) -> List[Tuple[int, int]]:
        """
        Convert human cell addresses to grid cell numbers

        Args:
            cell_names (List[str]): list of a boat type positions e.g. ["B3-C3", "D6-E6", "C8-E8"]
            boat_size (int): boat size

        Return:
            List(Tuple(int, int)): list of the boats positions on the grid

        Raises:
            ConfigurationException: if values were invalid
        """

        positions = []
        for cell_name in cell_names:
            pos = cell_name.split("-")
            if len(pos) > 2:
                raise ConfigurationException(
                    ErrorMessageCode.PLAYER_CONFIGURATION_INVALID_CELL_NAME.format(
                        self._get_error_message(cell_name)
                    )
                )
            if len(pos) == 1:
                # one size boat e.g. A3
                positions.append(self._get_position_on_board(pos[0]))
            else:
                # more than one size boat e.g. A3-D3
                start = self._get_position_on_board(pos[0])
                end = self._get_position_on_board(pos[1])
                if start[0] == end[0]:  # the same column
                    orientation = "v"
                    size = end[1] - start[1] + 1
                    if size != boat_size:
                        raise ConfigurationException(
                            ErrorMessageCode.PLAYER_CONFIGURATION_INVALID_CELL_NAME.format(
                                self._get_error_message(cell_name), boat_size
                            )
                        )
                elif start[1] == end[1]:
                    orientation = "h"  # the same row
                    size = end[0] - start[0] + 1
                    if size != boat_size:
                        raise ConfigurationException(
                            ErrorMessageCode.PLAYER_CONFIGURATION_INVALID_CELL_NAME.format(
                                self._get_error_message(cell_name), boat_size
                            )
                        )
                else:
                    # invalid addressing
                    raise ConfigurationException(
                        ErrorMessageCode.PLAYER_CONFIGURATION_INVALID_CELL_NAME.format(
                            self._get_error_message(cell_name)
                        )
                    )
                positions.append((start, end, orientation))
        return positions

    def load_configuration(self) -> None:
        """
        load configuration file and convert human fleet address to grid indexes
        This method feeds self.fleet_configuration method

        Raises:
            ConfigurationException: if configuration file or data was invalid
        """
        # read config file
        data = read_file(self.config_file_name)
        try:
            json_data = json.loads(data)
        except JSONDecodeError:
            # raise error if config file is invalid
            raise ConfigurationException(
                ErrorMessageCode.INVALID_CONFIGURATION.format(
                    self._get_error_message(self.config_file_name)
                )
            )
        # check missed boats
        fleets_set = set(self.fleet_configuration)
        missed_boats = fleets_set - set(json_data.keys())
        if missed_boats:
            raise ConfigurationException(
                ErrorMessageCode.PLAYER_CONFIGURATION_MISSED_BOAT.format(
                    self._get_error_message(missed_boats)
                )
            )
        # check invalid boats
        invalid_boats = set(json_data.keys()) - fleets_set
        if invalid_boats:
            raise ConfigurationException(
                ErrorMessageCode.PLAYER_CONFIGURATION_INVALID_BOAT.format(
                    self._get_error_message(missed_boats)
                )
            )

        for boat_type in json_data:
            boats = json_data[boat_type]
            # checks for each boat type boat number is equals of that type quantity
            if len(boats) != self.fleet_configuration[boat_type.lower()]["quantity"]:
                raise ConfigurationException(
                    ErrorMessageCode.PLAYER_CONFIGURATION_INVALID_BOAT_NUMBER.format(
                        self._get_error_message(boat_type)
                    )
                )
            # control cell name and boat size
            self.fleet_positions[boat_type] = self._get_boats_positions(
                boats, self.fleet_configuration[boat_type.lower()]["size"]
            )

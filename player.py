from typing import List, Tuple, NewType
from board import Board
from boat import Boat
from exceptions import ConfigurationException
from errors import ErrorMessageCode


class Player(object):
    def __init__(
        self,
        label: str,
        board_size: int,
        fleet_configurations: dict,
        player_fleet_positions: dict,
    ):
        """
        Create a Player instance

        Args:
            label (str): It refers to Player name
            board_size (int): board size
            default_fleet_configurations: default fleet configuration contains fleet size and quantities
            player_fleet_positions: player fleet positions on the board
        """

        self.board_size: int = board_size
        self.player_name: str = label
        self.fleet_configs: dict = fleet_configurations
        total_boat_count = 0
        for config in fleet_configurations.values():
            total_boat_count += config["size"] * config["quantity"]
        self.board: Board = Board(board_size, total_boat_count)
        self.opponent: Player = None
        self.fleet_positions: List[Tuple[int]] = player_fleet_positions
        self.fleet: List[Boat] = []

    def __repr__(self):
        return self.player_name

    def create_fleet(self) -> None:
        """
        Creates boat objects and add them to fleets list
        fleets_position_sample = {
              "battleship": [((4, 3), (7, 3), 'h')],
              "cruiser": [((0, 4), (0, 6), 'v'), ((7, 6), (9, 6), 'h')],
              "destroyer": [((1, 2), (2, 2), 'h'), ((3, 5), (4, 5), 'h'), ((3, 7), (4, 7), 'h')],
              "submarine": [(5, 0), (3, 9), (5, 9), (7, 9)]
        }
        """

        for boat_type in self.fleet_positions:
            for boat_position in self.fleet_positions[boat_type]:
                if len(boat_position) == 2:
                    # size 1 boat
                    boat = Boat(
                        label=boat_type,
                        size=self.fleet_configs[boat_type]["size"],
                        start_position=boat_position,
                        end_position=boat_position,
                        orientation="v",
                    )
                else:
                    # size 2 and more
                    boat = Boat(
                        label=boat_type,
                        size=self.fleet_configs[boat_type]["size"],
                        start_position=boat_position[0],
                        end_position=boat_position[1],
                        orientation=boat_position[2],
                    )
                self.fleet.append(boat)

    def locate_boats_on_board(self) -> None:
        """
        locating boats on the player's board
        """
        self.create_fleet()
        for boat in self.fleet:
            self.board.add_boat(boat)

    def set_opponent(self, opponent) -> None:
        """
        Sets player's opponent
        """
        self.opponent: Player = opponent

    def attack(self, col: int, row: int) -> bool:
        """
        Attacks to opponent

        Args:
            row (int): row number to attack
            col (int): column number to attack

        Returns:
            Tuple[bool, Boat]: returns (True, boat_obj) if hits boat, (False, None) if failed
        """
        if not self.opponent:
            raise ConfigurationException(ErrorMessageCode.MISSING_PLAYER_OPPONENT)
        return self.opponent.board.fire(row=row, col=col)

    @property
    def is_winner(self) -> bool:
        """
        define if player is winner
        """
        return self.opponent.board.is_defeat

    @property
    def success_hits(self) -> int:
        return self.opponent.board.success_hits

    @property
    def no_winner(self) -> bool:
        """

        Returns: no win after all the shots taken from file

        """
        return True
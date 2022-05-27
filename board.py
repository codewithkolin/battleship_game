from typing import Tuple
from boat import Boat
from errors import ErrorMessageCode
from exceptions import ConfigurationException
from helper import get_cell_name

FREE_SIGN = "."
BOAT_SIGN = "B"
HIT_SIGN = "X"
MISSED_SIGN = "0"


class Board(object):
    def __init__(self, size: int, total_boat_count: int):
        self.size = size
        self.grid = [[FREE_SIGN] * size for i in range(size)]
        self.success_hits = 0
        self.failed_hits = 0
        self.total_boat_on_board = total_boat_count

    def __repr__(self):
        str_val = "   " + " ".join([str(i) for i in range(self.size)]) + "\n"
        for i in range(self.size):
            str_val += str(i) + "  "
            for j in range(self.size):
                if isinstance(self.grid[i][j], Boat):
                    str_val += BOAT_SIGN + " "
                else:
                    str_val += self.grid[i][j] + " "
            if i != self.size - 1:
                str_val += "\n"
        return str_val

    def _check_neighbors(self, row: int, col: int) -> bool:
        """
        checks a position's neighbors and returns True if neighbors were free

        Args:
            row (int): row number for check
            col (int): column number for check

        Returns:
            bool: returns True if can add boat to the position

        Raises:
            ConfigurationException: if the cell or its adjacent is occupied
        """
        if self.grid[row][col] != FREE_SIGN:
            raise ConfigurationException(
                ErrorMessageCode.BOARD_CELL_OCCUPIED.format(get_cell_name(col, row))
            )
        if row > 0 and self.grid[row - 1][col] != FREE_SIGN:
            raise ConfigurationException(
                ErrorMessageCode.BOARD_CELL_ADJACENT.format(get_cell_name(col, row))
            )
        if row < self.size - 1 and self.grid[row + 1][col] != FREE_SIGN:
            raise ConfigurationException(
                ErrorMessageCode.BOARD_CELL_ADJACENT.format(get_cell_name(col, row))
            )
        if col > 0 and self.grid[row][col - 1] != FREE_SIGN:
            raise ConfigurationException(
                ErrorMessageCode.BOARD_CELL_ADJACENT.format(get_cell_name(col, row))
            )
        if col < self.size - 1 and self.grid[row][col + 1] != FREE_SIGN:
            raise ConfigurationException(
                ErrorMessageCode.BOARD_CELL_ADJACENT.format(get_cell_name(col, row))
            )
        return True

    def add_boat(self, boat: Boat) -> None:
        """
        Adds one boat to the board

        Args:
            boat (Boat): boat instance to add on the board

        Raises:
            ConfigurationException: if there was any occupation on the location
        """
        # size 1
        if boat.size == 1:
            # makes sure location does not occupied and does not have adjacent boat
            self._check_neighbors(boat.start_position[1], boat.start_position[0])
            self.grid[boat.start_position[1]][boat.start_position[0]] = boat
        else:
            # makes sure location does not occupied and does not have adjacent boat
            self._check_neighbors(boat.start_position[1], boat.start_position[0])
            self._check_neighbors(boat.end_position[1], boat.end_position[0])
            for x in range(boat.size):
                if boat.orientation == "h":
                    self.grid[boat.start_position[1]][boat.start_position[0] + x] = boat
                elif boat.orientation == "v":
                    self.grid[boat.start_position[1] + x][boat.start_position[0]] = boat

    def fire(self, row: int, col: int) -> Tuple[bool, Boat]:
        """
        Fire to the position

        Args:
            row (int): row number to attack
            col (int): column number to attack

        Returns:
            Tuple[bool, Boat]: returns (True, boat_obj) if hits boat, (False, None) if failed
        """
        # See what is currently at this position.
        if self.grid[row][col] == FREE_SIGN:
            self.failed_hits += 1
            return False, None
        elif self.grid[row][col] == HIT_SIGN:
            return False, None
        else:  # boat
            self.success_hits += 1
            boat = self.grid[row][col]
            self.grid[row][col] = HIT_SIGN
            return True, boat

    @property
    def is_defeat(self) -> bool:
        """
        Is the board defeated?
        """
        return self.success_hits == self.total_boat_on_board

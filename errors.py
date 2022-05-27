class ErrorMessageCode(object):
    """Error messages keep under this class"""

    OSERROR = "OS error occurred trying to open {}"
    MISSING_ARG_PLAYER1 = "Please enter the Player1 configuration file.!"
    MISSING_ARG_PLAYER2 = "Please enter the Player2 configuration file."
    MISSING_ARG_FIRSTPLAYER = "Please determine first player!"
    MISSING_ARG_SHOTS = "Please enter a list of shots that separated with space!"
    MISSING_PLAYER_OPPONENT = "The player" "s opponent is not defined!"

    INVALID_ARG_FIRSTPLAYER = "First player must be either P1 or P2 value"
    INVALID_CONFIGURATION = "{} configuration file is invalid!"
    INVALID_BOARD_SIZE = "The board size is invalid. The maximum size is 26"
    INVALID_FLEET_CONFIGURATION = "Fleet configuration is invalid!"
    INVALID_FILE_NAME = "File {} does not exists!"

    PLAYER_CONFIGURATION_MISSED_BOAT = "{} boat information is missed!"
    PLAYER_CONFIGURATION_INVALID_BOAT = "{} boat information is invalid!"
    PLAYER_CONFIGURATION_INVALID_BOAT_NUMBER = "{} boat number is invalid"
    PLAYER_CONFIGURATION_INVALID_CELL_NAME = "{} is invalid name on the board!"
    PLAYER_CONFIGURATION_INVALID_BOAT_SIZE = (
        "{} invalid size for the boat. The size must be {}"
    )

    BOARD_CELL_OCCUPIED = "{} position is occupied by another boat. Invalid position!"
    BOARD_CELL_ADJACENT = "{} position has an adjacent boat. Invalid position!"

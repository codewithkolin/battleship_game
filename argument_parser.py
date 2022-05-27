import argparse
import os

from typing import List, Type, NewType
from errors import ErrorMessageCode

argument_type = NewType("argument_type", argparse.Namespace)


def parse_args(args: List[str]):
    """Parses arguments

    Args:
        args (List[str]): arguments name without application name

    Returns:
       argparse.Namespace : returns arguments
    """

    parser = argparse.ArgumentParser(description="A Battleship Simulation!")

    # defining arguments for parser object
    parser.add_argument(
        "-p1",
        "--player1",
        type=str,
        nargs=1,
        metavar="file_name",
        default=None,
        help="Player 1 board config file. It must be in json format.",
    )

    parser.add_argument(
        "-p2",
        "--player2",
        type=str,
        nargs=1,
        metavar="file_name",
        default=None,
        help="Player 2 board config file. It must be in json format.",
    )

    parser.add_argument(
        "-f",
        "--firstplayer",
        type=str,
        nargs=1,
        metavar="P1 or P2",
        default=None,
        help="Specifics First player.",
    )

    parser.add_argument(
        "-s",
        "--shots",
        type=str,
        nargs="*",
        metavar="board_cell",
        default=None,
        help="All the board numbers separated by spaces will be added.",
    )

    parser.add_argument(
        "-sf",
        "--shotsfile",
        type=str,
        nargs=1,
        metavar="shots file name",
        default="",
        help="The file name contains shots list",
    )

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        nargs=1,
        metavar="file_name",
        default="game_config.json",
        help="Game configuration file name. It must be in json format.",
    )

    args = parser.parse_args(args)
    return args


def validate_args(args: argument_type) -> List[str]:
    """Primary validation to avoid missing argument

    Args:
        args (argparse.Namespace): arguments

    Returns:
       List[str] : returns a list of errors
    """
    messages = []
    if not args.player1:
        messages.append(ErrorMessageCode.MISSING_ARG_PLAYER1)
    if not args.player2:
        messages.append(ErrorMessageCode.MISSING_ARG_PLAYER2)
    if not args.firstplayer:
        messages.append(ErrorMessageCode.MISSING_ARG_FIRSTPLAYER)
    elif args.firstplayer and args.firstplayer[0].upper() not in ["P1", "P2"]:
        messages.append(ErrorMessageCode.INVALID_ARG_FIRSTPLAYER)
    if not args.shots and not args.shotsfile:
        messages.append(ErrorMessageCode.MISSING_ARG_SHOTS)
    # checks player 1 file exists on path
    if args.player1 and not os.path.exists(args.player1[0]):
        messages.append(ErrorMessageCode.INVALID_FILE_NAME.format(args.player1[0]))
    # checks player 2 file exists on path
    if args.player2 and not os.path.exists(args.player2[0]):
        messages.append(ErrorMessageCode.INVALID_FILE_NAME.format(args.player2[0]))
    # checks game config file exists on path
    game_config_file = args.config[0] if isinstance(args.config, list) else args.config
    if not os.path.exists(game_config_file):
        messages.append(ErrorMessageCode.INVALID_FILE_NAME.format(game_config_file))
    # checks if shots is a file, exists on path
    if len(args.shotsfile) == 1 and not os.path.exists(
        args.shotsfile[0]
    ):  # its file name
        messages.append(ErrorMessageCode.INVALID_FILE_NAME.format(args.shotsfile[0]))

    return messages

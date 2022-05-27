__auther__ = "Soheyla Ranjbar, soheyla.ranjbar2005@gmail.com"


import sys
from typing import List, Tuple
from argument_parser import parse_args, validate_args
from configuration import (
    GameConfiguration,
    PlayerBoardConfiguration,
    AddressingConfiguration,
    read_file,
)
from exceptions import ConfigurationException
from player import Player
import helper
from screenshot import ScreenShot
from boat import Boat


class BattleshipGame(object):
    def __init__(self, capture_screenshot: bool = True):
        args = parse_args(sys.argv[1:])
        errors = validate_args(args)
        for message in errors:
            print(">>>", message)
        if errors:
            exit()
        self.player1_name = "Player1"
        self.player2_name = "Player2"
        self.player1_config = args.player1[0]
        self.player2_config = args.player2[0]
        self.shots = args.shots
        self.shots_file = args.shotsfile[0] if args.shotsfile else None
        self.game_config = (
            args.config[0] if isinstance(args.config, list) else args.config
        )
        self.first_player = args.firstplayer[0].upper()
        self.screenshots = ScreenShot()
        self.capture_screen_shot = capture_screenshot

    @staticmethod
    def exit_game(e: ConfigurationException):
        print("\t FAILED!")
        print("\t", e.message)
        print("Simulation aborted!")
        exit()

    def play(self):
        print("*************** Welcome to BATTLESHIP! ***************")

        # load game configuration
        try:
            print("Validating Game Configuration: ")
            game_configuration: GameConfiguration = GameConfiguration(self.game_config)
            game_configuration.load_configuration()
            print("\t>>>> OK")
        except ConfigurationException as e:
            self.exit_game(e)

        # load player1 configuration
        try:
            print("Validating Player1 Configuration:")
            player1_config: PlayerBoardConfiguration = PlayerBoardConfiguration(
                player_label=self.player1_name,
                config_file_name=self.player1_config,
                board_size=game_configuration.size,
                fleet_configuration=game_configuration.fleet,
            )
            player1_config.load_configuration()
            player1: Player = Player(
                label=self.player1_name,
                board_size=game_configuration.size,
                fleet_configurations=player1_config.fleet_configuration,
                player_fleet_positions=player1_config.fleet_positions,
            )
            player1.locate_boats_on_board()
            self.screenshots.screen_shot(
                player1.board.grid, "Player1 - Initial status of the board"
            )
            print("\t>>>> OK")
        except ConfigurationException as e:
            self.exit_game(e)

        # load player1 configuration
        try:
            print("Validating Player2 Configuration:")
            player2_config = PlayerBoardConfiguration(
                player_label=self.player2_name,
                config_file_name=self.player2_config,
                board_size=game_configuration.size,
                fleet_configuration=game_configuration.fleet,
            )
            player2_config.load_configuration()
            player2: Player = Player(
                label=self.player2_name,
                board_size=game_configuration.size,
                fleet_configurations=player2_config.fleet_configuration,
                player_fleet_positions=player2_config.fleet_positions,
            )
            player2.locate_boats_on_board()
            self.screenshots.screen_shot(
                player2.board.grid, "Player2 - Initial status of the board"
            )
            print("\t>>>> OK")
        except ConfigurationException as e:
            self.exit_game(e)

        # set opponent
        player1.set_opponent(player2)
        player2.set_opponent(player1)

        # validating shots
        try:
            print("Validating Shots:")
            if not self.shots and self.shots_file:
                data = read_file(self.shots_file)
                self.shots = data.strip().split(" ")
            addressing_config = AddressingConfiguration(game_configuration.size)
            shots_positions: List[
                Tuple[int, int]
            ] = addressing_config.get_shots_positions(self.shots)
            print("\t>>>> OK")
        except ConfigurationException as e:
            self.exit_game(e)

        print("Starting the game")
        current_player = player1 if self.first_player == "P1" else player2
        print(f"{current_player.player_name} shoots first")
        # shoting
        for shot in shots_positions:
            shot_name = helper.get_cell_name(*shot)
            attack_result: Tuple[bool, Boat] = current_player.attack(
                col=shot[0], row=shot[1]
            )
            info = f"{current_player.player_name}: {shot_name} -> "
            if attack_result[0]:
                info += "Hit {}".format(attack_result[1].label.capitalize())
            else:
                info += "Miss"
            print(info)
            if current_player.is_winner:
                print(f"{current_player.player_name} won!")
                break
            # choose player turn, current player can continue if attack was successful
            current_player = (
                current_player if attack_result[0] else current_player.opponent
            )

        self.screenshots.screen_shot(
            player1.board.grid, "Player1 - Final status of the board"
        )
        self.screenshots.screen_shot(
            player2.board.grid, "Player2 - Final status of the board"
        )
        print(f"{player1.player_name} success hit count ->", player1.success_hits)
        print(f"{player2.player_name} success hit count ->", player2.success_hits)
        print("Simulation complete")
        if self.capture_screen_shot:
            self.screenshots.print_two_shot(
                "Player1 - Initial status of the board",
                "Player1 - Final status of the board",
            )
            self.screenshots.print_two_shot(
                "Player2 - Initial status of the board",
                "Player2 - Final status of the board",
            )


def main():
    """Entry point to the program"""
    game = BattleshipGame()
    game.play()


if __name__ == "__main__":
    # calling the main function
    main()

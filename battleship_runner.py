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
import random


class BattleshipGame(object):
    def __init__(self, capture_screenshot: bool = True):
        print("*************** Welcome to BATTLESHIP! ***************")
        args = parse_args(sys.argv[1:])
        if not args.interactive_play:
            errors = validate_args(args)
            for message in errors:
                print(">>>", message)
            if errors:
                exit()
            self.player1_config = args.player1[0]
            self.player2_config = args.player2[0]
            self.player1_name = args.player1_name[0]
            self.player2_name = args.player2_name[0]
            self.p1_shots_file = 'p1_shots.txt'
            self.p2_shots_file = 'p2_shots.txt'
            self.game_config = args.config
            self.board_size = args.board_size
            if type(args.board_size) == list:
                self.board_size = args.board_size[0]
        if args.interactive_play:
            print("Let start interactive gameplay.\n")
            self.player1_name = str(input("Player 1 please enter your name.\n"))
            self.player2_name = str(input("Player 2 please enter your name.\n"))
            self.player1_config = 'player1_board.json'
            self.player2_config = 'player2_board.json'
            self.game_config = 'game_config.json'
            self.board_size = args.board_size
            if type(args.board_size) == list:
                self.board_size = args.board_size[0]
        self.screenshots = ScreenShot()
        self.capture_screen_shot = capture_screenshot
        self.option = args.interactive_play

    @staticmethod
    def exit_game(e: ConfigurationException):
        print("\t FAILED!")
        print("\t", e.message)
        print("Simulation aborted!")
        exit()

    def play(self):
        # load game configuration
        try:
            print("Validating Game Configuration: ")
            game_configuration: GameConfiguration = GameConfiguration(self.board_size, self.game_config, self.option)
            game_configuration.load_configuration()
            if self.option:
                print("enter 1 for default Fleet location.")
                print("enter 2 for custom input Fleet location")
                opt = int(input("Please input above option"))
                print("Grabbing Player Fleet location: ")
                if opt != 1:
                    print("{} input you fleet location".format(self.player1_name))
                    self.player1_config = game_configuration.fleet_position(game_configuration.fleet, self.player1_name)
                    print("{} input you fleet location".format(self.player2_name))
                    self.player2_config = game_configuration.fleet_position(game_configuration.fleet, self.player2_name)
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
                player1.board.grid, "{} - Initial status of the board".format(player1.player_name))
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
                player2.board.grid, "{} - Initial status of the board".format(player2.player_name))
            print("\t>>>> OK")
        except ConfigurationException as e:
            self.exit_game(e)

        # set opponent
        player1.set_opponent(player2)
        player2.set_opponent(player1)
        current_player = random.choice([player1, player2])
        # validating shots
        if not self.option:
            p1_data = read_file(self.p1_shots_file)
            p2_data = read_file(self.p2_shots_file)
            ret1 = validating_shots(p1_data.strip().split(" "), game_configuration.size)
            ret2 = validating_shots(p2_data.strip().split(" "), game_configuration.size)
        self.all_shots_p1 = []
        self.all_shots_p2 = []
        print("Starting the game")
        print("{} will start the game first.".format(current_player.player_name))
        while not current_player.is_winner:
            if self.option:
                try:
                    print("{} is calling shots now".format(current_player.player_name))
                    while True:
                        try:
                            self.shots = []
                            self.shots.append(
                                str(input("{} please enter location where you want to hit.\n".format(current_player.player_name))))
                            if current_player == player1:
                                self.all_shots_p1.append(self.shots[0])
                                if self.all_shots_p1.count(self.shots[0]) < 2:
                                    break
                                else:
                                    self.all_shots_p1.remove(self.shots[0])
                            if current_player == player2:
                                self.all_shots_p2.append(self.shots[0])
                                if self.all_shots_p2.count(self.shots[0]) < 2:
                                    break
                                else:
                                    self.all_shots_p2.remove(self.shots[0])
                            print("Please enter unused location.")
                        except Exception as e:
                            print(e)
                    shots_positions = validating_shots(self.shots, game_configuration.size)
                    # if not len(self.shots):
                    #     raise Exception("Shots called was empty.")yes
                except ConfigurationException as e:
                    self.exit_game(e)
            else:
                try:
                    if current_player == player1:
                        shots_positions = ret1
                    if current_player == player2:
                        shots_positions = ret2
                except ConfigurationException as e:
                    self.exit_game(e)
            # print("Validating Shots:")
            # addressing_config = AddressingConfiguration(game_configuration.size)
            # shots_positions: List[
            #     Tuple[int, int]
            # ] = addressing_config.get_shots_positions(self.shots)
            # print("\t>>>> OK")
            print("Starting the game")
            print(f"{current_player.player_name} shoots first")
            shot_name = helper.get_cell_name(*shots_positions[0])
            attack_result: Tuple[bool, Boat] = current_player.attack(col=shots_positions[0][0], row=shots_positions[0][1])
            info = f"{current_player.player_name}: {shot_name} -> "
            if attack_result[0]:
                info += "Hit {}".format(attack_result[1].label.capitalize())
                print(info)
            else:
                info += "Miss"
            print(info)
            if current_player.is_winner:
                print(f"{current_player.player_name} won!")
                break
            # choose player turn, current player can continue if attack was successful
            if not self.option:
                if current_player == player1:
                    ret1.remove(shots_positions[0])
                else:
                    ret2.remove(shots_positions[0])
            current_player = (
                current_player if attack_result[0] else current_player.opponent
            )
            if not self.option:
                if 0 in (len(ret1), len(ret2)):
                    print(f"{player1.player_name} success hit count ->", player1.success_hits)
                    print(f"{player2.player_name} success hit count ->", player2.success_hits)
                    print(player1.player_name + " won!" if player1.success_hits >player2.success_hits else player2.player_name + " won!")
                    break
        self.screenshots.screen_shot(
            player1.board.grid, "{} - Final status of the board".format(player1.player_name))
        self.screenshots.screen_shot(
            player2.board.grid, "{} - Final status of the board".format(player2.player_name))
        print(f"{player1.player_name} success hit count ->", player1.success_hits)
        print(f"{player2.player_name} success hit count ->", player2.success_hits)
        print("Simulation complete")
        if self.capture_screen_shot:
            self.screenshots.print_two_shot(
                "{} - Initial status of the board".format(player1.player_name),
                "{} - Final status of the board".format(player1.player_name),
            )
            self.screenshots.print_two_shot(
                "{} - Initial status of the board".format(player2.player_name),
                "{} - Final status of the board".format(player2.player_name),
            )

def validating_shots(shot,game_config):
    print("Validating Shots:")
    addressing_config = AddressingConfiguration(game_config)
    shots_positions: List[
        Tuple[int, int]
    ] = addressing_config.get_shots_positions(shot)
    print("\t>>>> OK")
    return shots_positions



def main():
    """Entry point to the program"""
    game = BattleshipGame()
    game.play()


if __name__ == "__main__":
    # calling the main function
    main()

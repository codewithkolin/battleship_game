# battleship

## Agenda:
- How to run the project
- Command line parameters
- Configuration files format
- System architecture

## Run the project

There is 2 ways to run this project.

1. Download the project from git repo.
    1. Open cmd and type `git clone https://github.com/sumank450/battleship_game.git`
    2. Download the zip file of repo https://github.com/sumank450/battleship_game.git and extract it.
    3. You can use any IDE to get the repo using git(Pycharm).


2. Using Docker.
   1. Please install docker desktop to run the dockerized file.
   
   2. Because the project was dockerized, you can use the following command to get an interactive shell:
      1. If you haven't changed the argument in dockerfile, Game will run without any user input.
        
            To Run `$ docker-compose run --rm battleship`
      2. If you have added "-i", "True" in CMD ["python", "battleship_runner.py", "-p1_name", "Player1" ,"-p1", "player1_board.json", "-p2_name", "Player2", "-p2", "player2_board.json", "-f", "P2"]
            
            To Run:
         1. `$ docker compose build battleship`
         2. `$ docker run -i -t battleship`       
 
 The container and image are named `battleship`.
 
 After running docker compose you can run program by running `battleship_runner.py` file.
 
 here is an example of the command for running game:
 
 `$ python battleship_runner.py -p1_name Player1 -p1 player1_board.json -p2_name Player2 -p2 player2_board.json -b 10 -f P1`
 
 ## Command line parameters
 by typing  `python battleship_runner.py -h` list of parameters will show.
 
 |Description |Argument |Argument |
 |----------: |:-------:| :-------:|
 |Defining Player1 name.
 The name must be string | -p1_name Player1 | --player1_name Player1|
 |Defining the name of the Player1 configuration file.
 The file must be in json format.| -p1 [file_name.json]| --player1 [file_name.json]|
 |Defining Player2 name.
 The name must be string | -p2_name Player2 | --player2_name Player2|
 |Defining the name of the Player2 configuration file..
 The file must be in json format. | -p2 [file_name.json]| --player2 [file_name.json]|
 |Defining the first player.
 The value must be either P1 or P2| -f [P1 or P2] | --firstplayer [P1 or P2]|
 |Changing the game's default values of board size
 The value must be in range (2,26) | -b 10 | --board_size 10|
 |To change default value ofboat types, boat size, and boat quantity.
 The file must be in json format.| -c [file_name.json] | --config [file_name.json]|
 
**Note:**
- For non-interactive gameplay.
  * There are two files. p1_shots.txt and p2.shots.txt
- For interactive gameplay.
  * Shots are called each time per current player turn.
- The --config parameter isn't necessary.
You must send the new configuration file to the program if you want to modify the game's default board size and fleet.
- There are sample configuration files in the project:
    - player1_board.json -> defines player1 fleet positions.
    - player2_board.json -> defines player2 fleet positions.
    - game_config.json -> defines the game configuration (board size, boat types, each boat's size and quantity).

## Configuration files format
### Game configuration file
This file must be a json file with a format like the following:
```json
{
  "board": {
    "size": 10
  },
  "boat": {
    "battleship": {
      "size": 4, "quantity": 1
    },
    "cruiser": {
      "size": 3, "quantity": 2
    },
    "destroyer": {
      "size": 2, "quantity": 3
    },
    "submarine": {
      "size": 1, "quantity": 4
    }
  }
}
```

Under the boat section, you can define boat types and their size and quantity.
Please be aware that the application will use this section information to match players' config files boat types with the game's valid boat types.

### Player's configuration file
This file must be a json file with a format like the following:
```json
{
  "battleship": ["E4-H4"],
  "cruiser": ["A5-A7", "H7-J7"],
  "destroyer": ["B3-C3", "D6-E6", "D8-E8"],
  "submarine": ["F1", "D10", "F10", "H10"]
}
```
If the name of each boat type, as well as its size and quantity, do not match the values given in the game configuration, the game will display an error message and then quit.

### Player Shots list file
This file must be a simple text file with one line, that contains shots list. For example:
```
B5 D8 B2 F9 A9 C6 D7 G8 F2 B4 A8 B3 D4 F4 E2 I2 E8 C10 A8 E2 H4 B1 E1 G5 E3 E6 J6 C9 H10 D2 G9 C10 D5 B1
```

## System Architecture
In this section, I attempt to describe my analysis and architecture implementation.

### 1- First Analysing
By reading the assignment, it was obvious that the program must have 4 classes in its inside:
1. Board
2. Boat
3. Player
    
    Each player will have their own board, and an opponent who is also a player.
4. Game Controller

    The central point that binds all the components together.

Also, we can refer these facts from the requirement document:
* We need to read arguments' inputs, thus we'll need an argument parser to collect the arguments and do a basic validation on them.
* Because configuration will be defined via a file, we'll need a class that reads the file and validates its data.

After preparing everything we can start game by these steps:
1. Creating a game configuration model by reading and validating game configuration.
2. Reading the configuration of Player1 and validating the fleet configurations according to the game configuration in step 1.
3. Reading the configuration of Player2 and validating the fleet configurations according to the game configuration in step 1.
4. Locating players boats on the board, validating the adjacent criteria.
5. Making them as each other opponent.
6. Reading and validating each player shots file.
7. Defining who will start first.
8. For each shot:
    - Attacking to the opponent board
    - Showing the attack result
    - Defining turn
    - Monitoring of whether a player has won

### 2- Implementation
I drew a business analysis and algorithm stages up until this point.
I realized that the program requires many messages to represent the client's failure or success conditions, 
therefore I decided to create a class to containing these messages.
The benefit of this technique is that if I decide to alter an error message one day, I only have to edit it at one place.
I placed error messages in `errors.py` file.

`argument_parser.py` contains methods for gathering and validating arguments.

Reading, validating configuration files are implemented in `configuration.py` file.

The properties of boats are kept in `boat.py`. In the class of boat, I override the equals method, which was utilized in the test cases.

Adding boat on the board, controlling the adjacent criterias, fire, and the boat defeat status is implemented in `board.py`.

Players' essential actions are implemented in `player.py`, such as locating the player's boat on his/her board, setting the opponent, and attacking the opponent's board.

And finally the game will play inside _BattleshipGame_ class that located at `battleship_runner.py`.

Tests are under development. Will be released in future.

**Thank you for your time and consideration**

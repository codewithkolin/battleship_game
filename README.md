# battleship

## Aganda:
- How to run the project
- Command line parameters
- Configuration files format
- System architecture

## Run the project
Because the project was dockerized, you can use the following command to get an interactive shell:
 
 `$ docker-compose run --rm battleship`
 
 The container and image are named `battleship`.
 
 After running docker compose you can run program by running `battleship_runner.py` file.
 
 here is an example of the command for running game:
 
 `$ python battleship_runner.py -p1 player1_board.json -p2 player2_board.json -f P1 -s A1 A2 A4 A6 A8 A9 A10 B1 B3 B5 ...`
 
 ## Command line parameters
 by typing  `python battleship_runner.py -h` list of parameters will show.
 
 |Description |Argument |Argument |
 |----------: |:-------:| :-------:|
 |Defining the name of the Player1 configuration file.
 The file must be in json format.| -p1 [file_name.json]| --player1 [file_name.json]|
|Defining the name of the Player2 configuration file..
The file must be in json format. | -p2 [file_name.json]| --player2 [file_name.json]|
|Defining the first player.
The value must be either P1 or P2| -f [P1 or P2] | --firstplayer [P1 or P2]|
|Defining list of shots. | -s [shots list e.g. A1 B2 D3]| --shots [shots list e.g. A1 B2 D3]|
|Defining the file that contains shots.
The file must be an simple text file.| -sf [file_name.txt]| --shotsfile [file_name.txt]|
|Changing the game's default values such as board size, boat types, boat size, and boat quantity.
The file must be in json format.| -c [file_name.json] | --config [file_name.json]|
 
**Note:**
- You can specify shots with the -s argument or by using a file.
If you give both of them as inputs, the application will prioritize the --shots parameter values.
- The --config parameter isn't necessary.
You must send the new configuration file to the program if you want to modify the game's default board size and fleet.
- There are sample configuration files in the project:
    - player1_board.json -> defines player1 fleet positions.
    - player2_board.json -> defines player2 fleet positions.
    - game_config.json -> defines the game configuration (board size, boat types, each boat's size and quantity).
    - shots.txt -> The list of the shots for playing game.

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

Under the board.size section, you can define board size. The default value is 10.
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

### Shots list file
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

    Each player will have their own board and an opponent who is also a player.
4. Game Controller

    The central point that binds all of the components together.

Also we can refer these facts from the requirement document:
* We need to read arguments' inputs, thus we'll need an argument parser to collect the arguments and do a basic validation on them.
* Because configuration will be defined via a file, we'll need a class that reads the file and validates its data.

After preparing everything we can start game by these steps:
1. Creating a game configuration model by reading and validating game configuration.
2. Reading the configuration of Player1 and validating the fleet configurations according to the game configuration in step 1.
3. Reading the configuration of Player2 and validating the fleet configurations according to the game configuration in step 1.
4. Locating players boats on the their board, validating the adjacent criteria.
5. Making them as each other opponent.
6. Reading and validating shots file/list.
7. Defining who will start first.
8. For each shots:
    - Attacking to the opponent board
    - Showing the attack result
    - Defining turn
    - Monitoring of whether or not a player has won

### 2- Implementation
I drew a business analysis and algorithm stages up until this point.
I realized that the program requires a large number of messages to represent the client's failure or success conditions, 
therefore I decided to create a class to containing these messages.
The benefit of this technique is that if I decide to alter an error message one day, I only have to edit it at one place.
I placed error messages in `errors.py` file.

`argument_parser.py` contains methods for gathering and validating arguments.

Reading, validating configuration files are implemented in `configuration.py` file.

The properties of boats are kept in `boat.py`. In the class of boat, I override the equals method, which was utilized in the test cases.

Adding boat on the board, controlling the adjacent criterias, fire, and the boat defeat status is implemented in `board.py`.

Players' essential actions are implemented in `player.py`, such as locating the player's boat on his/her board, setting the opponent, and attacking the opponent's board.

And finally the game will play inside _BattleshipGame_ class that located at `battleship_runner.py`.

Test cases are placed under _tests_ folder.

**Thank you for your time and consideration**

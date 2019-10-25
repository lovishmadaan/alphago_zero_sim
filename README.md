# Alpha Go Zero Simulator

Simulator and competition code for COL870(Reinforcement Learning)


### Environment Simulator

> Env is hacked from Atari Py.

The simulator and environment code is present in `goSim.py`

- **Basic functions**
    - `reset()`: Reset the environment such that player 1 is BLACK and player 2 is WHITE
    - `step(a_t)`: Take an action `a_t` in environment (board in our case)
    - `render()`: Returns a string to be printed on screen. (Ignore komi value being printed)
    - `close()`: close the `env`
- **State vs Observation**
    - `state`: is what is maintained by Simulator
    - `observation`: is what you will get in return from `step(a_t)` function. Observation is `3 * board_size * board_size` representing where is black, white and empty spaces (Figure out which one is which)
    - Keeping a context of past will be your responsibility, `env` will always return only current observation
- **Action: integer between `[0, board_size^2 + 1]`**
    - Passing action `a` to `step()`: board position will be `(a // board_size, a % board_size)`
    - Passing `board_size^2` to `step()`: It will mean pass action
    - Passing `board_size^2 + 1`: It will mean resign action
- **Special mention**
    - Two consecutive pass actions by players means game is terminated
    - If player one passes but player two does not pass then player one can pass again next time and vice versa.




### Summarizing basic details

- **Printing observation**
    - `X -> BLACK`
    - `O -> WHITE`
    - `. -> Empty`
- **Player id**
    - BLACK = 1
    - WHITE = 2
- **Special Actions**
    - `pass_action` = `board_size^2`    
    - `resign_action` = `board_size^2 + 1`

### Requirements from each submission

All your code should be in the `alphago_zero_sim` folder. This directory should contain a file named `AlphaGoPlayer_<group_id>.py`. `group_id` is the one from your paper presentation groups. If you have extra code files required by `AlphaGoPlayer_<group_id>.py`, these should be put in `utils_<group_id>` folder and imported accordingly. Given below is the folder hierarchy:

    alphago_zero_sim
    ├── AlphaGoPlayer_<group_id>.py       # Your implementation for AlphaGoPlayer
    └── utils_<group_id>                  # directory containing any helper code required by AlphaGoPlayer

The `AlphaGoPlayer_<group_id>.py` should contain:

* `class AlphaGoPlayer():` This class should contain `init_state` (initial state of the board), `seed` (seed for initializations in your training) and `player_color` (integer, BLACK: 1 and WHITE: 2)

* `def get_action(s_t):` Given the current state of the board as input, this returns an action taken by your player on the board, integer between `[0, board_size^2 + 1]`

We have provided you a sample of AlphaGoPlayer: `AlphaGoPlayer_1.py` and `AlphaGoPlayer_2.py`

### Running a single match instance

`single_match.py` contains the class `SingleMatch()`, which is initialized by `board_size`, `komi_value` and the `match_directory` (directory location for the match between 2 opponents). It has the following functions:

* `get_action(s_t)`: used to obtain the action by a particular player from `AlphaGoPlayer_<group_id>.py`.

* `run_match()`: Runs 1 match instance between the 2 players(player order decided in `tournament.py`). Returns winner, score after the match is completed(positive score indicates white player won and negative score indicates black player won) and writes the history of actions taken by each player in `actions.csv`

> NOTE: If you want to run `single_match.py`, you will have to import `AlphaGoPlayer`. `tournament.py` takes care of this by making a temporary python file depending on which pair of players are selected.

### How to run the Tournament

`tournament.py` contains the classes `Tournament()` and `RunMatches()`. `Tournament()` is used to play between all players taken two at a time and `RunMatches()` is used to play the matches between a particular pair of players.

Description of the classes and functions:

* `class RunMatches()`: initialized by `player1` and `player2` (integers), `num_matches` (number of matches to be played between each pair), `root_folder` (directory location for the 2 players), `board_size` and `komi_value`.

* `def run_matches()`: calls `single_match` function for `num_matches` times, where each player is the first player alternatively.

* `class Tournament()`: initialized by `student_list` (integer list of students), `num_matches`, `board_size` and `komi_value`. Creates a directory named `Tournament` after initialization.

* `def run_tournament()`: calls the `run_matches` function for each pair of players.

# Environment Setup for HPC

Install Anaconda on HPC to make your life easier.

> NOTE: Anaconda for python3.6 is preferred(Anaconda3-5.2.0-Linux-x86_64.sh is the required script on Anaconda archives)

After installing Anaconda, follow the steps given below to install `gym` and `pachi_py` libraries required by your code.

```bash
conda create -n <env_name>
conda activate <env_name>
conda install pip
$HOME/anaconda3/envs/<env_name>/bin/pip install gym
module load apps/cmake/2.8.12/gnu
$HOME/anaconda3/envs/<env_name>/bin/pip install pachi-py
```

You should also install other libraries required by your code like `numpy`. Make sure that you mention these on Piazza so that we can install these on our HPC systems to grade for the tournament.
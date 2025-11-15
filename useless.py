import random
import sys
import time # Import the time module
random.seed()
import numpy as np

from games import Game, GameState

def minmax_decision(state, game, depthLim = 3):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    player = game.to_move(state)

    def max_value(state, depthLimIn):
        if game.terminal_test(state) or depthLimIn <=0:
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), depthLimIn-1))
        return v

    def min_value(state, depthLimIn):
        if game.terminal_test(state) or depthLimIn <=0:
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), depthLimIn -1))
        return v

    return max(game.actions(state), key=lambda a: min_value(game.result(state, a), depthLim))


def alpha_beta_search(state, game, depth_limit=10):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if depth <= 0 or game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if depth <= 0 or game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, depth_limit)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action

def random_player(game, state, depth):
    """A player that chooses a legal move at random."""
    return random.choice(game.actions(state)) if game.actions(state) else None


def alpha_beta_player(game, state, depth):
    return alpha_beta_search(state, game, depth)


def minmax_player(game,state, depth):
    return minmax_decision(state,game, depth)


class Mancala(Game):
    def __init__(self, players = [alpha_beta_player, random_player], pits_per_player=6, stones_per_pit = 4, depth = 5):
        self.pits_per_player = pits_per_player
        self.board = [stones_per_pit] * ((pits_per_player+1) * 2)
        
        self.current_player = 1
        self.moves = []
        self.p1_pits_index = [0, self.pits_per_player-1]
        self.p1_mancala_index = self.pits_per_player
        self.p2_pits_index = [self.pits_per_player+1, len(self.board)-1-1]
        self.p2_mancala_index = len(self.board)-1
        
        self.board[self.p1_mancala_index] = 0
        self.board[self.p2_mancala_index] = 0
        
        self.initial = GameState(to_move = "1", utility = 0, board = self.board.copy(), moves=())
        self.state = self.initial
        
        self.players = players
        self.depth = depth
        
        # Track moves per player
        self.p1_moves = 0
        self.p2_moves = 0

    def valid_move(self, pit, state):
        """
        Function to check if the pit chosen by the current_player is a valid move.
        """
        if state.to_move == "1":
            pit_index = pit - 1
            if pit_index < self.p1_pits_index[0] or pit_index > self.p1_pits_index[1]:
                return False
        else:
            pit_index = self.p2_pits_index[1] - (pit - 1)
            if pit_index < self.p2_pits_index[0] or pit_index > self.p2_pits_index[1]:
                return False
        
        return list(state.board)[pit_index] > 0
    
    def terminal_test(self, state):
        """Function to verify if the game board has reached the winning state."""
        board = list(state.board) if state.board else self.board
        
        p1_pits_sum = sum(board[self.p1_pits_index[0]:self.p1_pits_index[1]+1])
        p2_pits_sum = sum(board[self.p2_pits_index[0]:self.p2_pits_index[1]+1])
        
        return p1_pits_sum == 0 or p2_pits_sum == 0
    
    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        val = []
        for pit in range(1, self.pits_per_player + 1):
            if (self.valid_move(pit, state)): 
                val.append(pit)
        return val

    def utility(self, state, player):
        """Return the value of this final state to player."""
        if (player == "1"): return list(state.board)[self.p1_mancala_index] - list(state.board)[self.p2_mancala_index]
        else: return list(state.board)[self.p2_mancala_index] - list(state.board)[self.p1_mancala_index]

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        board = list(state.board)
        
        if state.to_move == "1":
            pit_index = move - 1
            my_pits_range = self.p1_pits_index
            my_mancala = self.p1_mancala_index
            opponent_mancala = self.p2_mancala_index
        else:
            pit_index = self.p2_pits_index[1] - (move - 1)
            my_pits_range = self.p2_pits_index
            my_mancala = self.p2_mancala_index
            opponent_mancala = self.p1_mancala_index
        
        stones = board[pit_index]
        board[pit_index] = 0
        
        current_index = pit_index
        
        while stones > 0:
            current_index = (current_index + 1) % len(board)
            if current_index == opponent_mancala:
                continue
            board[current_index] += 1
            stones -= 1
        
        next_player = "2" if state.to_move == "1" else "1"
    
        # continuation rule
        if current_index == my_mancala:
            next_player = state.to_move
        elif my_pits_range[0] <= current_index <= my_pits_range[1] and board[current_index] == 1:
            opposite_index = len(board) - 2 - current_index
            if board[opposite_index] > 0:
                captured = board[current_index] + board[opposite_index]
                board[current_index] = 0
                board[opposite_index] = 0
                board[my_mancala] += captured
        
        self.board = board.copy()
        
        return GameState(to_move=next_player, utility=0, board=tuple(board), moves=())
    
    def display(self):
        """
        Displays the board in a user-friendly format
        """
        player_1_pits = self.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]
        player_1_mancala = self.board[self.p1_mancala_index]
        player_2_pits = self.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]
        player_2_mancala = self.board[self.p2_mancala_index]

        print('P1             P2')
        print('      ____{}____     '.format(player_2_mancala))
        for i in range(self.pits_per_player):
            if i == self.pits_per_player - 1:
                print('{} -> |_{}_|_{}_| <- {}'.format(i+1, player_1_pits[i], 
                                player_2_pits[-(i+1)], self.pits_per_player - i))
            else:     
                print('{} -> | {} | {} | <- {}'.format(i+1, player_1_pits[i], 
                                player_2_pits[-(i+1)], self.pits_per_player - i))
            
        print('          {}           '.format(player_1_mancala))
        turn = 'P1' if self.state.to_move == "1" else 'P2'
        print('Turn: ' + turn)
        
    def play_game(self):
        """Play an n-person, move-alternating game."""
        while True:
            if self.state.to_move == "1":
                player = self.players[0]
                self.p1_moves += 1
            else:
                player = self.players[1]
                self.p2_moves += 1
                
            move = player(self, self.state, self.depth)
            self.state = self.result(self.state, move) 
            
            if self.terminal_test(self.state):
                score_diff = list(self.state.board)[self.p1_mancala_index] - list(self.state.board)[self.p2_mancala_index]
                return {
                    'score_diff': score_diff,
                    'p1_moves': self.p1_moves,
                    'p2_moves': self.p2_moves,
                    'total_moves': self.p1_moves + self.p2_moves,
                    'winner': 1 if score_diff > 0 else (2 if score_diff < 0 else 0)  # 0 = tie
                }


# Run trials and collect statistics
num_trials = 100
depth = 5

score_diffs = []
p1_wins = 0
p2_wins = 0
ties = 0
p1_moves_list = []
p2_moves_list = []
total_moves_list = []

# --- ETA Setup ---
start_time = time.time()
# The trial count after which we consider the speed calculation stable enough
# to start showing ETA. (e.g., after 100 trials)
ETA_CALC_THRESHOLD = 100 

def format_time(seconds):
    """Converts a time in seconds to a human-readable HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    sec = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{sec:02d}"
# -----------------

print(f"Running {num_trials} trials with depth = {depth}...")
# print(f"Player 1: Alpha-Beta | Player 2: Random\n")

for i in range(num_trials):
    mancala_game = Mancala(players = [alpha_beta_player, random_player], depth=depth)
    result = mancala_game.play_game()
    
    score_diffs.append(result['score_diff'])
    p1_moves_list.append(result['p1_moves'])
    p2_moves_list.append(result['p2_moves'])
    total_moves_list.append(result['total_moves'])
    
    if result['winner'] == 1:
        p1_wins += 1
    elif result['winner'] == 2:
        p2_wins += 1
    else:
        ties += 1

    # --- Progress Bar and ETA Update ---
    current_trials = i + 1
    percent = current_trials / num_trials * 100
    
    progress_str = f"\rProgress: {current_trials}/{num_trials} trials run ({percent:.2f}%)"
    
    if current_trials >= ETA_CALC_THRESHOLD:
        elapsed_time = time.time() - start_time
        # Speed in trials per second
        trials_per_second = current_trials / elapsed_time
        
        remaining_trials = num_trials - current_trials
        # Estimated remaining time in seconds
        eta_seconds = remaining_trials / trials_per_second
        
        eta_str = format_time(eta_seconds)
        elapsed_str = format_time(elapsed_time)
        
        # Add ETA and Elapsed Time to the progress string
        progress_str += f" | Elapsed: {elapsed_str} | ETA: {eta_str}"

    sys.stdout.write(progress_str)
    sys.stdout.flush()
    # -----------------------------------

# Print a final newline character to ensure the following output starts on a new line
print()

# Print results
print("============================================================")
print("TRIAL RESULTS")
print("============================================================")
print(f"\nTotal Games Played: {num_trials}")
print(f"\nWin Statistics:")
print(f"  Player 1 Wins: {p1_wins} ({p1_wins/num_trials*100:.1f}%)")
print(f"  Player 2 Wins:      {p2_wins} ({p2_wins/num_trials*100:.1f}%)")
print(f"  Ties:               {ties} ({ties/num_trials*100:.1f}%)")

print(f"\nScore Difference Statistics (P1 - P2):")
print(f"  Total Sum:      {sum(score_diffs)}")
print(f"  Average:        {np.mean(score_diffs):.2f}")
print(f"  Std Dev:        {np.std(score_diffs):.2f}")
print(f"  Min:            {min(score_diffs)}")
print(f"  Max:            {max(score_diffs)}")

print(f"\nMoves Statistics:")
print(f"  Average P1 Moves per Game:     {np.mean(p1_moves_list):.2f}")
print(f"  Average P2 Moves per Game:     {np.mean(p2_moves_list):.2f}")
print(f"  Average Total Moves per Game: {np.mean(total_moves_list):.2f}")
print(f"  Total P1 Moves (all games):    {sum(p1_moves_list)}")
print(f"  Total P2 Moves (all games):    {sum(p2_moves_list)}")
print(f"  Total Moves (all games):       {sum(total_moves_list)}")

print("============================================================")
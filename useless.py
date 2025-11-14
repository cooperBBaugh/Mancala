import random
random.seed()
from games import *

class Mancala(Game):
    def __init__(self, pits_per_player=6, stones_per_pit = 4):
        """
        The constructor for the Mancala class defines several instance variables:

        pits_per_player: This variable stores the number of pits each player has.
        stones_per_pit: It represents the number of stones each pit contains at the start of any game.
        board: This data structure is responsible for managing the Mancala board.
        current_player: This variable takes the value 1 or 2, as it's a two-player game, indicating which player's turn it is.
        moves: This is a list used to store the moves made by each player. It's structured in the format (current_player, chosen_pit).
        p1_pits_index: A list containing two elements representing the start and end indices of player 1's pits in the board data structure.
        p2_pits_index: Similar to p1_pits_index, it contains the start and end indices for player 2's pits on the board.
        p1_mancala_index and p2_mancala_index: These variables hold the indices of the Mancala pits on the board for players 1 and 2, respectively.
        """
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
        
        self.players = [minmax_player, random_player]

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
        
        # return self.board[pit_index] > 0
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
        # print(val)
        return val

    def utility(self, state, player):
        """Return the value of this final state to player."""
        if (state.to_move == "1"): return list(state.board)[self.p1_mancala_index] - list(state.board)[self.p2_mancala_index]
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
        
        if current_index != my_mancala:
            if my_pits_range[0] <= current_index <= my_pits_range[1] and board[current_index] == 1:
                opposite_index = len(board) - 2 - current_index
                if board[opposite_index] > 0:
                    captured = board[current_index] + board[opposite_index]
                    board[current_index] = 0
                    board[opposite_index] = 0
                    board[my_mancala] += captured
        
        # Update self.board for actual game display
        self.board = board.copy()
        
        next_player = "2" if state.to_move == "1" else "1"
        return GameState(to_move=next_player, utility=0, board=tuple(board), moves=())
    
    def display(self):
        """
        Displays the board in a user-friendly format
        """
        player_1_pits = self.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]
        player_1_mancala = self.board[self.p1_mancala_index]
        player_2_pits = self.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]
        player_2_mancala = self.board[self.p2_mancala_index]

        print('P1               P2')
        print('     ____{}____     '.format(player_2_mancala))
        for i in range(self.pits_per_player):
            if i == self.pits_per_player - 1:
                print('{} -> |_{}_|_{}_| <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            else:    
                print('{} -> | {} | {} | <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            
        print('         {}         '.format(player_1_mancala))
        turn = 'P1' if self.state.to_move == "1" else 'P2'
        print('Turn: ' + turn)
          
    def play_game(self):
        """Play an n-person, move-alternating game."""
        while True:
            if self.state.to_move == "1":
                player = self.players[0]  # Player 1
            else:
                player = self.players[1]  # Player 2
            print("PLAYER b4")
            print(player)
            move = player(self, self.state)
            self.state = self.result(self.state, move) 
            print("PLAYER after")
            print(player)
            # self.display()
            if self.terminal_test(self.state):
                # self.display()
                # self.display(self.state)
                print(list(self.state.board)[self.p1_mancala_index] - list(self.state.board)[self.p2_mancala_index])
                return list(self.state.board)[self.p1_mancala_index] - list(self.state.board)[self.p2_mancala_index]

trials = []
for i in range(100):
  mancala_game = Mancala(pits_per_player=6, stones_per_pit=4)
  trials.append(mancala_game.play_game())

print(trials)



  # def play(self, pit):
  #         """
  #         Simulated a play in Mancala
  #         """
  #         if not self.valid_move(pit):
  #             print("INVALID MOVE")
  #             return self.board
          
  #         if self.winning_eval():
  #             print("GAME OVER")
  #             return self.board
          
  #         self.moves.append((self.current_player, pit))
          
  #         if self.current_player == 1:
  #             pit_index = pit - 1
  #             my_pits_range = self.p1_pits_index
  #             my_mancala = self.p1_mancala_index
  #             opponent_mancala = self.p2_mancala_index
  #             opponent_pits_range = self.p2_pits_index
  #         else:
  #             pit_index = self.p2_pits_index[1] - (pit - 1)
  #             my_pits_range = self.p2_pits_index
  #             my_mancala = self.p2_mancala_index
  #             opponent_mancala = self.p1_mancala_index
  #             opponent_pits_range = self.p1_pits_index
          
  #         stones = self.board[pit_index]
  #         self.board[pit_index] = 0
          
  #         current_index = pit_index
          
  #         while stones > 0:
  #             current_index = (current_index + 1) % len(self.board)
  #             if current_index == opponent_mancala:
  #                 continue
  #             self.board[current_index] += 1
  #             stones -= 1
          
  #         if current_index != my_mancala:
  #             if my_pits_range[0] <= current_index <= my_pits_range[1] and self.board[current_index] == 1:
  #                 opposite_index = len(self.board) - 2 - current_index
  #                 if self.board[opposite_index] > 0:
  #                     captured = self.board[current_index] + self.board[opposite_index]
  #                     self.board[current_index] = 0
  #                     self.board[opposite_index] = 0
  #                     self.board[my_mancala] += captured
              
  #         self.current_player = 2 if self.current_player == 1 else 1
          
  #         return self.board

#def random_move_generator(self):
    #     """
    #     Function to generate random valid moves with non-empty pits for the random player
    #     """
    #     import random
    #     valid_pits = []
    #     for pit in range(1, self.pits_per_player + 1):
    #         if self.valid_move(pit):
    #             valid_pits.append(pit)
    #     return random.choice(valid_pits) if valid_pits else None
    
    
    
    
# def run_mancala_trials(numTrials):
#     moves_per_game = []
#     p1_wins = 0
#     p2_wins = 0
#     ties = 0

#     num_trials = numTrials

#     for i in range(num_trials):

#         game = Mancala(pits_per_player=6, stones_per_pit=4)

#         p1_moves_played = 0
#         p2_moves_played = 0

#         while not game.winning_eval():
#             if game.current_player == 1:
#                 game.play(game.random_move_generator())
#                 p1_moves_played += 1
#             else:
#                 game.play(game.random_move_generator())
#                 p2_moves_played += 1
        
#         moves_per_game.append((p1_moves_played, p2_moves_played))

#         if game.board[game.p1_mancala_index] > game.board[game.p2_mancala_index]:
#             p1_wins += 1
#         elif game.board[game.p1_mancala_index] < game.board[game.p2_mancala_index]:
#             p2_wins += 1

#     # # results

#     p1_win_percentage = p1_wins / num_trials * 100
#     p2_win_percentage = p2_wins / num_trials * 100

#     p1_avg_moves = sum([x for (x,y) in moves_per_game]) / num_trials
#     p2_avg_moves = sum([y for (x,y) in moves_per_game]) / num_trials

#     print(f"Trials: {numTrials}")

#     print("Player 1 Statistics:")
#     print(f"Win percentage: %{p1_win_percentage}")
#     print(f"Loss percentage: %{p2_win_percentage}")
#     print(f"Tie percentage: %{100 - p1_win_percentage - p2_win_percentage}")
#     print(f"Average # of moves: {p1_avg_moves}")

#     print("")

#     print("Player 2 Statistics:")
#     print(f"Win percentage: %{p2_win_percentage}")
#     print(f"Loss percentage: %{p1_win_percentage}")
#     print(f"Tie percentage: %{100 - p1_win_percentage - p2_win_percentage}")
#     print(f"Average # of moves: {p2_avg_moves}")
# run_mancala_trials(100)
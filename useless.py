  # def display_board(self):
    #     """
    #     Displays the board in a user-friendly format
    #     """
    #     player_1_pits = self.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]
    #     player_1_mancala = self.board[self.p1_mancala_index]
    #     player_2_pits = self.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]
    #     player_2_mancala = self.board[self.p2_mancala_index]

    #     print('P1               P2')
    #     print('     ____{}____     '.format(player_2_mancala))
    #     for i in range(self.pits_per_player):
    #         if i == self.pits_per_player - 1:
    #             print('{} -> |_{}_|_{}_| <- {}'.format(i+1, player_1_pits[i], 
    #                     player_2_pits[-(i+1)], self.pits_per_player - i))
    #         else:    
    #             print('{} -> | {} | {} | <- {}'.format(i+1, player_1_pits[i], 
    #                     player_2_pits[-(i+1)], self.pits_per_player - i))
            
    #     print('         {}         '.format(player_1_mancala))
    #     turn = 'P1' if self.current_player == 1 else 'P2'
    #     print('Turn: ' + turn)

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
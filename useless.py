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
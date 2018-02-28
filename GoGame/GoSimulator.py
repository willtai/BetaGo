from . import GoBackend
import numpy as np
from Shared.Consts import WHITE, BLACK, EMPTY, num_to_char, char_to_num
from Shared.Functions import toggle_player

class GoSimulator:

    def __init__(self, N):
        GoBackend.set_size(N)
        self.N = N
        self.board = GoBackend.Position.initial_state()

    def _board_to_string(self, board):
        board_flat = board.reshape((self.N**2))
        board_str = ''.join(list((map(lambda x: num_to_char[x], board_flat))))
        return board_str


    def set_board_from_prev_boards(self, prev_boards, next_player):
        last_player = toggle_player(next_player)
        board1 = self._board_to_string(prev_boards[-2])
        board2 = self._board_to_string(prev_boards[-1]) 
        ko = GoBackend.Position.find_ko(board1, board2, last_player)
        self.set_board(prev_boards[-1], next_player)

    def set_board(self, board, next_player, ko=None):
        board_str = self._board_to_string(board)
        ko_flat = None
        if ko is not None:
            ko_flat = ko[0]*self.N + ko[1]
        self.board = GoBackend.Position.set_board(board=board_str,ko=ko_flat)
        self.current_player = next_player

    def play(self, x, y):
        self.board = self.board.play_move(x*self.N+y, self.current_player)
        self.current_player = toggle_player(self.current_player)
        return (self.as_array(), self.current_player)

    def pass_move(self):
        self.current_player = toggle_player(self.current_player)
        return (self.as_array(), self.current_player)

    def as_array(self):
        char_list = list(self.board.board)
        num_list = list(map(lambda x: char_to_num[x], char_list))
        board_array = np.array(num_list).reshape((self.N, self.N))
        return board_array

    def get_legal_moves(self):
        legal = self.board.get_legal_moves()
        _, ko = self.board
        if ko is not None:
            legal[ko] = 0
        return np.array(legal).reshape((self.N,self.N))

    def print_board(self):
        print(self.board)

    def black_score_lead(self):
        '''Black Score - White Score'''
        return self.board.score()






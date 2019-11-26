from default_player import *
from rule_checker import *
from board import *
import copy
from global_variables import BOARD_LENGTH, string_to_tuple
import random


class Referee:
    def __init__(self,player1 = player(), player2 = player()):
        self.player1 = player1
        self.player2 = player2
        self.boardHistory = [[[' '] * BOARD_LENGTH for i in range(BOARD_LENGTH)]]
        self.currentPlayer = 'B'
        self.RC = rule_checker()
        self.game_start = False

    def game_state(self):
        return self.game_start
    
    def set_player1_name(self, name):
        self.player1.set_name(name)
        self.player1.set_stone("B")
        return self.player1.get_stone()
    
    def set_player2_name(self, name):
        self.player2.set_name(name)
        self.player2.set_stone("W")
        return self.player2.get_stone()
    
    def start_game(self):
        self.game_start = True
        self.player1.set_stone('B')
        self.player2.set_stone('W')
        return self.boardHistory
    
    def check_and_make_move(self,coordinate):
        winner = []
        if coordinate == "pass":
            self.boardHistory = [self.boardHistory[0]] + self.boardHistory
            if len(self.boardHistory) > 3:
                self.boardHistory = self.boardHistory[:3]
            self.currentPlayer = "B" if self.currentPlayer == "W" else "W"
        
        elif self.RC.check_if_move_valid(self.currentPlayer, coordinate, self.boardHistory):
            B = Board(copy.deepcopy(self.boardHistory[0]))
            B.place(self.currentPlayer, coordinate)
            self.currentPlayer = "B" if self.currentPlayer == "W" else "W"
            self.RC.take_out_stones_without_liberty(self.currentPlayer, B)
            newBoard = B.board
            self.boardHistory = [newBoard] + self.boardHistory
            if len(self.boardHistory) > 3:
                self.boardHistory = self.boardHistory[:3]
            
        else:
            winner = [self.player2] if self.currentPlayer == self.player1.get_stone() else [self.player1]

        if winner:
            self.game_start = False
            return [winner[0].get_name()]
        
        if self.RC.check_if_board_history_valid(self.currentPlayer,self.boardHistory):
            return self.boardHistory
        else:
            B = Board(self.boardHistory[0])
            score = B.find_score() 
            
            if score['W'] > score['B']:
                winner = [self.player2]
            elif score['W'] < score['B']:
                winner = [self.player1]
            else:
                winner = [self.player1, self.player2]
            self.game_start = False
            result = [player.get_name() for player in winner]
            result.sort()
            return result
            #

    def start_match(self):
        winner, cheater = [], None
        p1, p2 = self.player1, self.player2
        
        try:
            name1, name2 = p1.get_name(), p2.get_name()
            board_history = self.start_game()
            while self.game_state(): 
                if 'B' == self.currentPlayer:
                    move = p1.make_move(board_history)
                    board_history = self.check_and_make_move(string_to_tuple(move))
                    
                else:
                    move = p2.make_move(board_history)   
                    board_history = self.check_and_make_move(string_to_tuple(move))
        except Exception as e:
            print(e)
            cheater = name1 if self.currentPlayer == 'B' else name2
            winner = name1 if self.currentPlayer == 'W' else name2
        
        #reset players so they can play the next game
        self.player1.state = 'registered'
        self.player2.state = 'registered'
        
        #print(self.boardHistory)
        if not winner:
            winner = board_history[0]
        
        if len(winner) == 2:
            random.seed(0)
            winner = random.choice(winner)
        return winner, cheater
        

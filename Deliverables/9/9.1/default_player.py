from rule_checker import *
from board import *
from abc import ABC, abstractmethod
import socket
import json
import pickle
from global_variables import BOARD_LENGTH,Player_Exception,tuple_to_string
import random
class game_player(ABC):
    
    @abstractmethod
    def get_stone(self):pass

    def set_name(self,name):pass

    def set_stone(self, stone):pass

    def set_n(self, n):pass

    def get_name(self):pass

    def dummy_strategy(self, Boards):pass

    def capture_strategy(self, Boards):pass

    def capture(self, board, max_liberty):pass

    def find_smallest_coordinates(self, choices):pass

    def make_move(self, Boards):pass

    def register(self):pass
class player(game_player):
    def __init__(self, n=0):
        self.stone = ""
        self.name = "no name"
        self.opponent = ""
        self.RC = rule_checker()
        self.n = n
        self.current_n = n
        self.state = None
    
    def get_stone(self):
        return self.stone
        
    def set_name(self,name):
        self.name = name
    
    def set_stone(self, stone):
        if self.state == 'registered':
            self.stone = stone
            self.opponent = "B" if stone=="W" else "W"
            self.state = 'ready'
        else:
            #print(self.name)
            raise Player_Exception('try to set stone before player registered')

    def set_n(self, n):
        self.n = n

    def get_name(self):
        return self.name

    def register(self):
        if not self.state:
            self.state = 'registered'
            return self.get_name()
        else:
            raise Player_Exception('Register error')

    def dummy_strategy(self, Boards):
        if not self.RC.check_if_board_history_valid(self.stone, Boards): 
            return "This history makes no sense!"
        else:
            curBoard = Board(Boards[0])
            choice = []
            for i in range(BOARD_LENGTH):
                for j in range(BOARD_LENGTH):
                    if self.RC.check_if_move_valid(self.stone,(i,j),Boards): 
                        choice.append((i,j))
            if len(choice) > 1:
                return random.choice(choice)
            return "pass"
    
    def capture_strategy(self, Boards):
        if not self.RC.check_if_board_history_valid(self.stone, Boards): 
            return "This history makes no sense!"
        if self.n==1: 
            curBoard = Board(Boards[0])
            opponent_stones = curBoard.reverse_get_points(curBoard.get_points(self.opponent)) 
            choices = []
            
            for (i,j) in opponent_stones:
                liberty, free_coords = curBoard.find_liberty((i,j)) 
                if liberty == 1 and self.RC.check_if_move_valid(self.stone,free_coords[0],Boards): choices.append(free_coords[0]) 
            if choices: 
                return self.find_smallest_coordinates(choices) 
        elif self.n>1: 
            if self.current_n == 0: self.current_n=self.n
            choices = self.capture(Boards[0], self.current_n)
            if choices: 
                self.current_n -= 1
                return self.find_smallest_coordinates(choices)        
        return self.dummy_strategy(Boards)

    def testing_strategy1(self, board_history):
        num = random.randint(1,100)
        if num < 50:
            return 'the is a invalid move'
        else:
            return self.dummy_strategy(board_history)

    # return a list of possible coordinates we can choose given self.n
    # return T /F, if T adds to the list of possible coordinates
    def capture(self, board, max_liberty):
        curBoard = Board(board)
        opponent_stones = curBoard.reverse_get_points(curBoard.get_points(self.opponent)) 
        res = []
        for (i,j) in opponent_stones:
            liberty, free_coords = curBoard.find_liberty((i,j)) 
            if liberty <= max_liberty: 
                if max_liberty == 1: res.append(free_coords[0])
                else: 
                    for (i,j) in free_coords:
                        possible_Choice = True 
                        possible_Boards= []
                        newBoard = Board(board)
                        newBoard.place(self.stone, (i,j))
                        choices_for_opponent = list(filter(lambda x: x!= (i,j), free_coords))
                        
                        for (m,n) in choices_for_opponent: 
                            B = Board(newBoard.board)
                            B.place(self.opponent, (m,n))
                            liberty,_ = B.find_liberty((m,n))
                            if liberty > max_liberty: 
                                possible_Choice = False
                                break
                            else: possible_Boards.append(B)

                        if possible_Choice: 
                            should_include = True
                            for B in possible_Boards: 
                                if not self.capture(B, max_liberty-1): 
                                    should_include = False
                                    break
                            if should_include: res.append((i,j))
        return res

    # def check_liberity_for_opponent_move(self, board, choices,liberty_limit):
    #     B = Board(board)
    #     for (m,n) in choices: 
    #         B.place(self.opponent, (m,n))
    #         liberty,_ = B.find_liberty((m,n))
    #         if liberty > liberty_limit: return False
    #     return True

    def find_smallest_coordinates(self, choices):
        res = choices[0]
        for (i,j) in choices[1:]:
            if res[1] > j: 
                res = (i,j)
            elif res[1] == j and res[0] > i:
                res = (i,j)
        res = (res[1],res[0])
        return res 

    def make_move(self, Boards):
        if self.state == 'ready':
            if self.n==0: 
                move =  self.dummy_strategy(Boards)
            else: 
                move =  self.testing_strategy1(Boards)
            #print(move)
            move = tuple_to_string(move)
            #print(move)
            return move
        else:
            raise Player_Exception('player is not ready yet')
    def reset(self):
        self.state = 'registered'
        
    
class remote_player(player):
    def __init__(self, conn):
        self.conn = conn
        self.name = 'no name'
        #self.socket.listen()

    def register(self):
        mess = 'register'
        mess = json.dumps(mess)
        self.conn.send((mess.encode()))
        result = self.conn.recv(4096)
        result = result.decode()
        print(result)
        if not isinstance(result, str) or result == "GO has gone crazy!":
            raise Player_Exception('player has invalid name')
        
        self.name = result
        return result

    def set_stone(self,mess):
        mess = ['receive-stones',mess]
        mess = json.dumps(mess)
        self.conn.send((mess.encode()))
    
    def make_move(self, Board):
        mess = ['make-a-move',Board]
        mess = json.dumps(mess)
        self.conn.send((mess.encode()))
        result = self.conn.recv(6000).decode()
        return result

    def get_name(self):
        return self.name
    
    def reset(self):
        mess = ['end-game']
        mess = json.dumps(mess)
        try:
            self.conn.send((mess.encode()))
            result = self.conn.recv(6000).decode()
            if result != 'OK':
                self.clean_up()
        except:
            pass
        
    

    def clean_up(self):
        self.conn.close()
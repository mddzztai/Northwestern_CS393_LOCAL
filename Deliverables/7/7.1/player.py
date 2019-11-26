from rule_checker import *
from board import *
from abc import ABC, abstractmethod
import socket
import json
import pickle

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
    
    def get_stone(self):
        return self.stone
        
    def set_name(self,name):
        self.name = name
    
    def set_stone(self, stone):
        self.stone = stone
        self.opponent = "B" if stone=="W" else "W"

    def set_n(self, n):
        self.n = n

    def get_name(self):
        return self.name

    def register(self):
        return self.get_name()

    def dummy_strategy(self, Boards):
        if not self.RC.check_if_board_history_valid(self.stone, Boards): 
            return "This history makes no sense!"
        else:
            curBoard = Board(Boards[0])
            for j in range(19):
                for i in range(19):
                    if self.RC.check_if_move_valid(self.stone,(i,j),Boards): 
                        return (j,i)
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
        if self.n==0: 
            return self.dummy_strategy(Boards)
        else: 
            return self.capture_strategy(Boards)
    
class remote_player(player):
    
    def __init__(self, player, conn):
        self.player = player
        self.set_n()
        self.conn = conn
        #self.socket.listen()

<<<<<<< Updated upstream
    def close_connection(self):
        self.conn.close()
        
    def set_n(self):
        with open('go-player.config') as json_file:
            go_player_config = json.load(json_file)
        self.player.set_n(go_player_config['depth'])

    def remote_play(self,i):
        self.conn.send(pickle.dumps(i))
        result = pickle.loads(self.conn.recv(4096))
=======
    def register(self):
        self.conn.send(pickle.dumps('register'))
        result = pickle.load(self.conn.recv(4096))
        return result

    def set_stone(self,mess):
        self.conn.send(pickle.dumps(mess))
        result = pickle.load(self.conn.recv(4096))
        return result
    
    def make_move(self, mess):
        self.conn.send(pickle.dumps(mess))
        result = pickle.load(self.conn.recv(4096))
>>>>>>> Stashed changes
        return result
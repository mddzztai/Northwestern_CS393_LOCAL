from board import *
import copy

class rule_checker:
    def __init__(self):
        pass 
    
    def _check_valid_coordinate(self, coordinate: tuple) -> bool: 
        return 0 <= coordinate[0] < 19 and 0 <= coordinate[1] < 19
    
    def _check_valid_stone_type(self, stone):
        return stone in ["B", "W"]
    
    def _check_valid_maybeStone_type(self, maybeStone):
        return maybeStone in ["B", "W", " "]
    
    def check_pass(self, stone):
        return self._check_valid_stone_type(stone)
    
    def check_move(self, player, coordinate, board_history):
        return self.check_if_move_valid(player,coordinate, board_history) and self.check_if_board_history_valid(player,board_history)
    
    def check_if_move_valid(self, player, coordinate, board_history):
        if self._check_valid_coordinate(coordinate) and self._check_valid_stone_type(player):
            
            history = copy.deepcopy(board_history[0])

            B = Board(history)
            if B.if_occupied(coordinate): 
                return False
            connected, neighbors = B.find_connected_maybeStones(coordinate)
            if len(connected) > 1 or not neighbors: return True

            if not self.check_move_not_suicide(player, coordinate, B): 
                return False 
            
            # check if the new board will be the same as history 2
            if len(board_history) > 1:
                B.place(player, coordinate)
                opponent_stone = "W" if player =="B" else "B"
                self.take_out_stones_without_liberty(opponent_stone, B)

                b2 = Board(board_history[1])
                p4b, p4w = B.reverse_get_points(B.get_points("B")), B.reverse_get_points(B.get_points("W"))
                p2b, p2w = b2.reverse_get_points(b2.get_points("B")), b2.reverse_get_points(b2.get_points("W"))
                if p2b==p4b and p2w==p4w: 
                    return False
            
            return True 

        else:
            #print("invalid input")
            return False
        
    def check_move_not_suicide(self,player,coordinate,B):
        B2 = copy.deepcopy(B)
        B2.place(player, coordinate)
        _, neighbors = B2.find_connected_maybeStones(coordinate)
        for (x,y) in neighbors:
            if B2.board[x][y] == " ": return True
        visited = set()
        for neighbor_coordinate in neighbors:
            if neighbor_coordinate in visited: continue
            neighbor_connected, neighbor_neighbor = B2.find_connected_maybeStones(neighbor_coordinate)
            visited |= neighbor_connected
            for (x,y) in neighbor_neighbor:
                break_flag = False
                if B2.board[x][y] == " ": 
                    break_flag = True
                    break
            if not break_flag: return True     
        return False

    def check_if_board_history_valid(self, player, board_history):
        lg = len(board_history)
       
        if not lg: return False
        elif lg==1: 
            return self._check_empty_board(board_history[0]) and player=="B"
        elif lg==2:
            b2 =  Board(board_history[0])
            p2b, p2w = b2.get_points("B"), b2.get_points("W")
            return player=="W" and self._check_empty_board(board_history[1]) and len(p2b)<=1 and not len(p2w)
        elif lg>3:
            #print("Invalid number of board history given")
            return False 
        
        b3,b2,b1 = Board(board_history[0]), Board(board_history[1]), Board(board_history[2])
        # b3 represents the most recent board      

        if player == "W" and self._check_empty_board(board_history[1]) and self._check_empty_board(board_history[2]):
            return False
        if player == "W" and self._check_empty_board(board_history[2]) and b2.get_points("B"):
            return False
       
        p1b,p2b,p3b = b1.reverse_get_points(b1.get_points("B")) ,b2.reverse_get_points(b2.get_points("B")), b3.reverse_get_points(b3.get_points("B"))
        p1w,p2w,p3w = b1.reverse_get_points(b1.get_points("W")), b2.reverse_get_points(b2.get_points("W")), b3.reverse_get_points(b3.get_points("W"))
        
        if (p1b==p3b and p1w==p3w): return False
        
        compare_1_and_2, compare_2_and_3 = self.check_between_consecqutive_boards(b1, b2, p1b, p2b, p1w, p2w), self.check_between_consecqutive_boards(b2, b3, p2b, p3b, p2w, p3w)
        
        if not compare_1_and_2 or not compare_2_and_3:
            return False
        if compare_1_and_2 == compare_2_and_3:
            return False
        if player == compare_2_and_3:
            return False
        if compare_2_and_3 == " " and player != compare_1_and_2:
            return False
        for i in [b1, b2, b3]:
            if not self.check_board_not_contains_suicide(i): return False
        
        return True
         
    def check_between_consecqutive_boards(self, board1, board2, p1b, p2b, p1w, p2w):
        # check the difference between 2 boards, board2 is the most recent
        diff_b, add_b = self._check_diff_points(p1b, p2b)
        diff_w, add_w = self._check_diff_points(p1w, p2w)
        # find the stone that is added between 2 boards
        if len(add_b) + len(add_w) > 1: return False 
        if (diff_b and add_b) or (diff_w and add_w): return False 
        if not add_b and not add_w: move_stone = " "
        elif not add_b: move_stone = "W"
        else: move_stone = "B"
        
        if diff_b and diff_w: return False
        elif diff_b:
            diff = diff_b
            opponent_stone = "W"
        elif diff_w:
            diff = diff_w
            opponent_stone = "B"
        else: return move_stone

        
        connected, neighbors = set(),set()
        
        for (x,y) in diff:
            if (x,y) not in connected:
                local_connected, local_neighbors = board1.find_connected_maybeStones((x,y))
                connected |= local_connected
                neighbors |= local_neighbors
        
        for (x,y) in neighbors:
            if board2.board[x][y] != opponent_stone: return False

        connected, neighbors = set(),set()
        
        for (x,y) in diff:
            if (x,y) not in connected:
                local_connected, local_neighbors = board2.find_connected_maybeStones((x,y))
                connected |= local_connected
                neighbors |= local_neighbors
        
        for (x,y) in neighbors:
            if board2.board[x][y] != opponent_stone: return False

        return move_stone

    def _check_diff_points(self, p1, p2):
        stones = set(p1)
        add = []        
        
        for i in p2:
            if i in stones: stones.remove(i)
            else: add.append(i)
        
        return list(stones), add

    def check_board_not_contains_suicide(self, B):
        visited = set()
        for i in range(19):
            for j in range(19):
                if (i,j) in visited: continue
                connected, neighbors = B.find_connected_maybeStones((i,j))
                visited |= connected
                if B.board[i][j] == " ": continue
                liberty = False
                for (x,y) in neighbors:
                    if B.board[x][y] == " ":
                        liberty = True
                        break
                if not liberty: return False
        return True

    def _check_empty_board(self, board):
        for i in range(19):
                for j in range(19):
                    if board[i][j]!=' ': return False
        return True

    def take_out_stones_without_liberty(self, stone, B):
        to_remove = []
        for i in range(19):
            for j in range(19):
                if B.board[i][j]==stone and not B.find_liberty((i,j))[0]: 
                    to_remove.append([stone,(i,j)])
        
        for [stone, (i,j)] in to_remove:
            B.remove(stone,(i,j))
        return B
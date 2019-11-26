from global_length import BOARD_LENGTH
import typing

class Board:
    def __init__(self , board=[[' '] * BOARD_LENGTH for i in range(BOARD_LENGTH)] ):
        # initialize an BOARD_LENGTH * BOARD_LENGTH empty board
        self.board = board

    def _get_neighbors(self, coordinate: tuple) -> list:
        x, y = coordinate[0], coordinate[1]
        neighbors = []
        for (i,j) in [(-1,0),(1,0),(0,1),(0,-1)]:
            if 0 <= x+i < BOARD_LENGTH and 0 <= y+j < BOARD_LENGTH:
                neighbors.append((x+i, y+j))
        return neighbors
    
    def find_connected_maybeStones(self, coordinate):
        stoneType = self.board[coordinate[0]][coordinate[1]]
        stack = self._get_neighbors(coordinate)
        connected, visited, neighbors = set(), set(), set()
        connected.add(coordinate)
        visited.add(coordinate)
        # DFS
        while stack:
            (x,y) = stack.pop()
            visited.add((x,y))
            if stoneType == self.board[x][y]:
                connected.add((x,y))
                for (i,j) in self._get_neighbors((x,y)):
                    if (i,j) not in visited: 
                        stack.append((i,j))
            else: neighbors.add((x,y))
        return connected, neighbors
             

    def if_occupied(self,coordinate):
        x, y = coordinate[0], coordinate[1]
        return self.board[x][y] != " "
    
    
    def if_occupied_by_x(self,coordinate, stone):
        x, y = coordinate[0], coordinate[1]
        if self.board[x][y] == stone: return True
        else: return False


    def place(self, stone: str, coordinate: tuple):
        x, y = coordinate[0], coordinate[1]
        if self.board[x][y] != ' ':
            return "This seat is taken!"
        else:
            self.board[x][y] = stone
            return self.board

        
    def remove(self, stone: str, coordinate: tuple):
        x, y = coordinate[0], coordinate[1]
        if self.board[x][y] == stone:
            self.board[x][y] = " "
            return self.board
        else:
            return "I am just a board! I cannot remove what is not there!"
            

    def get_points(self, maybeStone: str):
        res = []
        for i in range(BOARD_LENGTH):
            for j in range(BOARD_LENGTH):
                if self.board[j][i]==maybeStone:
                    res.append((i,j))   
        return res 


    def find_score(self):
        res = {"B":0, "W":0}
        visited = set()
        for i in range(BOARD_LENGTH):
            for j in range(BOARD_LENGTH):
                if (i,j) not in visited:
                    visited.add((i,j))
                    stoneType = self.board[i][j]
                    if stoneType == "B": 
                        res["B"] += 1
                    elif stoneType == "W": 
                        res["W"] += 1
                    else: 
                        reach_B, reach_W = False, False 
                        connected, neighbors = self.find_connected_maybeStones((i,j))
                        for (m,n) in neighbors:
                            if self.board[m][n] == "B": 
                                reach_B=True 
                            elif self.board[m][n] == "W": 
                                reach_W=True 
                        visited |= connected
                        
                        if reach_B and reach_W: continue
                        elif reach_B: res["B"] += len(connected)
                        elif reach_W: res["W"] += len(connected)
        return res

    def reverse_get_points(self, points):
        for i in range(len(points)):
            points[i] = (points[i][1],points[i][0])
        return points

    def find_liberty(self, coordinate):
        _, neighbors = self.find_connected_maybeStones(coordinate)
        liberty = 0 
        free_coords = []
        for (i,j) in neighbors:
            if self.board[i][j] == " ": 
                liberty += 1
                free_coords.append((i,j))
        return liberty, free_coords

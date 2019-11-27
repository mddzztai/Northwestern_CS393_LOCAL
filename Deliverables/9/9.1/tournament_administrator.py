from global_variables import GET_PLAYERS_CONFIG
from referee import *
import socket
import sys
import importlib.util

def cal_rank(dict):
    # calculate the rank from the given scoreboard
    rank = []
    for name, score in dict.items():
        rank.append((score,name))
    rank.sort(reverse = True)
    rank_num = 0
    current_score = float('inf')

    for i in range(len(rank)):
        if rank[i][0] < current_score:
            rank_num += 1
            current_score = rank[i][0]
        rank[i] = (rank_num, rank[i][1])
    return rank

def main():
    # to decide the number of player in this tournament
    expo = 0
    while 2 ** expo < n:
        expo += 1
    total_n = 2 ** expo

    # ???question???: if n = 0, should we conduct the tournament
    if total_n <= 1:
        total_n = 2

    # the map that maps the name of player to the player object
    player = dict()

    # the count for local players
    local_player_count = 0
    
    # get the config
    add, p = GET_PLAYERS_CONFIG()

    #load the player class
    spec = importlib.util.spec_from_file_location("module.name", p)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    
    print('setting up the socket')
    
    # set up the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(add)
    s.listen(10)
    
    print('waiting for ' + str(n) + ' connections')
    
    for i in range(n):
        conn, _ = s.accept()
        rm_player = foo.remote_player(conn)
        name = rm_player.register()
        player[name] = rm_player
        print('remote player ' + str(i) +' has connected to the game')
    
    s.close()

    # set up the local players
    for _ in range(total_n):
        local_player = foo.player()
        local_player_count += 1
        local_player.set_name('local' + str(local_player_count))
        local_player.set_n(1)
        name = local_player.register()
        player[name] = local_player
    
    # round robin
    if match_type == '--league':
        score_board = [[(0,"")] * total_n] * total_n
        current_player_pool = []
        cheater_list = []
        for name in player:
            current_player_pool.append(name)
        for first_player_index in range(total_n):
            for second_player_index in range(first_player_index + 1, total_n):
                
                R = Referee(player[current_player_pool[first_player_index]], player[current_player_pool[second_player_index]])
                winner, cheater = R.start_match()
                # if the first player win
                if winner == current_player_pool[first_player_index]:
                    score_board[first_player_index][second_player_index] = (1, current_player_pool[second_player_index])
                    score_board[second_player_index][first_player_index] = (0, current_player_pool[first_player_index])
                else:
                    score_board[first_player_index][second_player_index] = (0, current_player_pool[second_player_index])
                    score_board[second_player_index][first_player_index] = (1, current_player_pool[first_player_index])
                
                #if there is one cheater
                if cheater:
                    cheater_index = first_player_index if cheater == current_player_pool[first_player_index] else second_player_index
                    for oppo_index in range(len(score_board[cheater_index])):
                        # change the score for the opponents that this cheater has defeated
                        
                        if score_board[cheater_index][oppo_index][0] == 1:
                            if score_board[oppo_index][cheater_index] != (-1, -1):
                                score_board[oppo_index][cheater_index] = (1, score_board[oppo_index][cheater_index][1]) 
                        
                        # make the previous game invalid
                        if score_board[cheater_index][oppo_index][1]:
                            score_board[cheater_index][oppo_index] = (-1, -1)

                        # switch the play if it is a remote player
                    
                    cheater_list.append(current_player_pool[cheater_index])
                    local_player_count += 1
                    local_player = foo.player()
                    local_player.set_name('local' + str(local_player_count))
                    name = local_player.register()
                    player[name] = local_player
                    current_player_pool[cheater_index] = name
           
            score = dict()

        for name in player:
            score[name] = 0
        
        for player_index in range(len(current_player_pool)):
            for oppo_index in range(len(current_player_pool)):
                if score_board[player_index][oppo_index][0] == 1:
                    score[current_player_pool[player_index]] += 1

        for name in cheater_list:
            score[name] = -1
            
        rank = cal_rank(score)
        # print(score_board)
        
        print(rank)


    # knock out
    else:
        score_board = {}
        prev_stage = []
        next_stage = []
        cheater_list = []
        find_champion = False
        for i in player:
            score_board[i] = 0
            prev_stage.append(i)
        
        while not find_champion:
            l, r = 0, len(prev_stage) - 1
            
            while l < r:
                R = Referee(player[prev_stage[l]], player[prev_stage[r]])
                winner, cheater = R.start_match()
                next_stage.append(winner)
                if cheater:    
                    cheater_list.append(cheater)
                for winner in next_stage:
                    score_board[winner] += 1
                
                l += 1
                r -= 1
            if len(next_stage) == 1:
                find_champion = True
            else:
                prev_stage = next_stage
                next_stage = []

        for name in score_board:
            if name in cheater_list:
                score_board[name] = -1
        
        rank = cal_rank(score_board)
        print(rank)
    
    for name in player:
        if isinstance(player[name], foo.remote_player):
            try:
                player[name].clean_up()
            except:
                continue

if __name__ == "__main__":
    if len(sys.argv) != 3:
        len_ = len(sys.argv)
        raise Exception('Wrong Number of Arguments ' + str(len_))
    _, match_type, n = sys.argv
    if match_type not in ['--league', '--cup']:
        raise Exception('Wrong Game Type ' + match_type)
    if not n.isnumeric():
        raise Exception('Please enter the valid format for remote player number')
    n = int(n)
    if n < 0 or n > 16:
        raise Exception('Wrong Number of players')
    main()
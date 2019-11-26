from referee import *
from board import *
import importlib.util
from global_length import Local_Exception, Remote_Exception

def string_to_tuple(s):
    if s == 'pass':
        return s
    a = s.split('-')
    return (int(a[1])-1, int(a[0])-1)


def GET_PLAYERS_CONFIG():
    with open('go.config') as json_file:
        go_config = json.load(json_file)
    
    IP_ADD = go_config['IP']
    port_num = go_config['port']
    
    server_ADD = (IP_ADD, port_num)
    return server_ADD, go_config['default-player']


def main():
    add, p = GET_PLAYERS_CONFIG()
    
    # load player() class
    spec = importlib.util.spec_from_file_location("module.name", p)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    
    #set up local player
    p1 = foo.player()
    #set up remote player
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(add)
    s.listen(1)
    conn, _ = s.accept()
    s.close()
    #
    p2 = foo.remote_player(conn)
    referee = Referee(p1, p2)
    
    winner = ''
    try:
        name1, name2 = p1.register(), p2.register()
        if not isinstance(name2, str):
            winner = name1
            raise Remote_Exception()
        board_history = referee.start_game()
        while referee.game_state():
            if 'B' == referee.currentPlayer:
                move = p1.make_move(board_history)   
                if isinstance(move,str):
                    if move != 'pass':
                        winner = name2
                        raise Local_Exception()
                elif not isinstance(move,tuple):
                    
                    winner = name2
                    raise Local_Exception()
                elif len(move) != 2 or move[0] < 0 or move[0] > 8 or move[1] < 0 or move[1] > 8 :
                    
                    winner = name2
                    raise Local_Exception()
                
                board_history = referee.check_and_make_move(move)
                
            else:
                move = p2.make_move(board_history)
                if isinstance(move,str):
                    if move == 'pass':
                        board_history = referee.check_and_make_move(string_to_tuple(move))
                    else:
                        c_flag = 0
                        if len(move) == 3:
                            if move[1] == '-':
                                if move[0].isnumeric() and move[2].isnumeric():
                                    if int(move[0]) != 0 and int(move[2]) != 0:
                                        
                                        c_flag = 1
                        if c_flag:
                            board_history = referee.check_and_make_move(string_to_tuple(move))
                        else:
                            raise Remote_Exception()    
                else:
                    raise Remote_Exception()    
                
                
    except(EOFError, BrokenPipeError) as e:
        winner = name1
    except Remote_Exception:
        winner = name1
    except Local_Exception:
        winner = name2
    
    if not winner:
        winner = board_history
    else:
        winner = [winner]
    winner = json.dumps(winner)
    print(winner)
    conn.close()
    p2.conn.close()
if __name__ == "__main__":
    main()
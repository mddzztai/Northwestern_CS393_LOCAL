from referee import *
from board import *
import importlib.util
from global_variables import Local_Exception, Remote_Exception


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
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # s.bind(add)
    # s.listen(1)
    # conn, _ = s.accept()
    # s.close()
    #
    p2 = foo.player()
    p1.set_name('123')
    p2.set_name('456')
    p1.set_n(0)
    p2.set_n(0)
    referee = Referee(p1, p2)
    
    winner = referee.start_match()
    winner = json.dumps(winner)
    
    print(winner)
    #conn.close()
    #p2.conn.close()
if __name__ == "__main__":
    main()
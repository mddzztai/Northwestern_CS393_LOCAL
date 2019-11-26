from rule_checker import *
from board import *
from player import *
import json
import sys
import socket
import pickle

def tuple_to_string(t):
    if isinstance(t,tuple):
        return str(t[0]+1) + '-' + str(t[1]+1)
    else: return t
 

def GET_SOCKET_CONFIG():
    with open('go.config') as json_file:
        go_config = json.load(json_file)
    
    IP_ADD = go_config['IP']
    port_num = go_config['port']
    
    server_ADD = (IP_ADD, port_num)
    return server_ADD

def main():
    #set up the port 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(GET_SOCKET_CONFIG())
    s.listen(1)
    conn, _ = s.accept()
    s.close()
    
    decoder = json.JSONDecoder()
    data_to_use = ''
    ret = []

    #read data in
    for data in sys.stdin: 
        data_to_use+= data.lstrip().rstrip('\n').rstrip() + ' '
    
    data = data_to_use.lstrip()
    p2 = remote_player(conn)
    try:
        while data:

            i,idx = decoder.raw_decode(data)

            data = data[idx:].lstrip()
            if i[0] == "receive-stones":
                
                mess = p2.remote_play(i)
                if not mess:
                    continue
                else:
                    ret.append(mess)
            else:
                result = p2.remote_play(i)
                ret.append(result)     
            if ret[-1] == "GO has gone crazy!": break

    except (EOFError, BrokenPipeError) as e:
        pass 
    p2.close_connection()
    conn.close()
    

    ret = json.dumps(ret)
    print(ret)


if __name__ == "__main__":
    main()
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

def read_json():
    
    input_list = [] 
    
    decoder = json.JSONDecoder()
    
    data_to_use = ''

    for data in sys.stdin: 
        
        data_to_use+= data.lstrip().rstrip('\n').rstrip() + ' '
            
    data = data_to_use.lstrip()
    while data:
        json_object,idx = decoder.raw_decode(data)
        input_list.append(json_object)	
        data = data[idx:].lstrip()	      

    return input_list

def main():
    #set up the port 
    with open('go.config') as json_file:
        go_config = json.load(json_file)
    
    IP_ADD = go_config['IP']
    port_num = go_config['port']
    
    server_ADD = (IP_ADD, port_num)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(server_ADD)
    s.listen(1)
    conn, _ = s.accept()
    s.close()
    #s.connect()
    #print('connection')
    ret = []

    data = read_json()
    #conn.send(pickle.dumps(len(data)))
    try:
        for i in data:
            if i[0] == "receive-stones":
                conn.send(pickle.dumps(i))
            else:
                conn.send(pickle.dumps(i))
                ret.append(pickle.loads(conn.recv(4096)))
    except (EOFError, BrokenPipeError) as e:
        pass

    
    
    
    conn.close()
    

    ret = json.dumps(ret)
    print(ret)


if __name__ == "__main__":
    main()
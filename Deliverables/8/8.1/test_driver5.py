from rule_checker import *
from board import *
from player import *
import json
import sys
import socket
import pickle
from threading import Thread

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

def func1(s, server_ADD):
    s.bind(server_ADD)
    s.listen(1)
    conn, _ = s.accept()
    return conn

def func2(s):
    p2 = remote_player(player(),s)
    return p2

def main():
    #set up the port 
    with open('go.config') as json_file:
        go_config = json.load(json_file)
    
    IP_ADD = go_config['IP']
    port_num = go_config['port']
    
    server_ADD = (IP_ADD, port_num)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    p2 = Thread(target=func2, args=[s]).start()
    
    Thread(target=func1, args=[s,server_ADD]).start()
    
    
    


if __name__ == "__main__":
    main()
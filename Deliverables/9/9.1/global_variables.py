import json
BOARD_LENGTH=9

class Local_Exception(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class Remote_Exception(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class Board_Exception(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class Player_Exception(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class Rule_Checker_Exception(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

def string_to_tuple(s):
    if s == 'pass':
        return s
    else:
        try:
            a = s.split('-')
        except:
            raise Player_Exception('invalid move')
    Tup = (int(a[1])-1, int(a[0])-1)
    if Tup >= (0,0) and Tup < (BOARD_LENGTH, BOARD_LENGTH):
        return Tup
    else:
        raise Player_Exception('Move out of board')

def tuple_to_string(tup):
    if isinstance(tup, str):
        return tup
    else:
        return str(tup[1] + 1) + '-' + str(tup[0] + 1)

def GET_PLAYERS_CONFIG():
    with open('go.config') as json_file:
        go_config = json.load(json_file)
    
    IP_ADD = go_config['IP']
    port_num = go_config['port']
    
    server_ADD = (IP_ADD, port_num)
    return server_ADD, go_config['default-player']
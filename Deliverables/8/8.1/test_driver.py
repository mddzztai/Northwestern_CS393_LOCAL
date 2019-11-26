from rule_checker import *
from board import *
from player import *
from referee import *
import json
import sys

def tuple_to_string(t):
    if isinstance(t,tuple):
        return str(t[0]+1) + '-' + str(t[1]+1)
    else: return t

def handle_input_str(s):
    if s == "pass":
        
        return s
    else:
        a = s.split('-')
        return (int(a[1])-1, int(a[0])-1)
def read_json():
    
    input_list = [] 
    num_json = 0
    
    decoder = json.JSONDecoder()
    
    data_to_use = ''

    for data in sys.stdin: 
        
        data_to_use+= data.lstrip().rstrip('\n').rstrip() + ' '
            
    data = data_to_use.lstrip()
    while data:
        json_object,idx = decoder.raw_decode(data)
        input_list.append(json_object)	
        num_json += 1
        data = data[idx:].lstrip()	      

    return input_list



def main():
    ret = []
    data = read_json()
    
    referee = Referee()
    
    for index, i in enumerate(data):
        if index == 0:
            ret.append(referee.set_player1_name(i))
        elif index == 1:
            ret.append(referee.set_player2_name(i))
            ret.append(referee.start_game())
        else:
            if referee.game_state():
                ret.append(referee.check_and_make_move(handle_input_str(i)))
            else:

                break
    # k = 0
    # print(ret[k])
    # print(len(ret))
    if referee.game_state():
        ret = ret[:-1]
    ret = json.dumps(ret)
    print(ret)

if __name__ == "__main__":
    main()


from player import *
import pickle

def tuple_to_string(t):
    if isinstance(t,tuple):
        return str(t[0]+1) + '-' + str(t[1]+1)
    else: return t

def reportInvalid(s):
    s.send(pickle.dumps('GO has gone crazy!'))

def main():
    with open('go.config') as json_file:
        go_config = json.load(json_file)
        
    IP_ADD = go_config['IP']
    port_num = go_config['port']
    
    server_ADD = (IP_ADD, port_num)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    s.connect(server_ADD)
    P = player()
    #data = pickle.loads(s.recv(4096))
    #len_ = i = pickle.loads(s.recv(4096))
    
    
    
    sequence_num = 0
    #some change to data to make a list
    try:
        while True:
            i = pickle.loads(s.recv(4096))
            
            if i[0] == "register":
                #not the first, len not equal to 1
                if sequence_num != 0 or len(i) != 1:
                    reportInvalid(s)
                    break
                s.send(pickle.dumps(P.register()))
            elif i[0] == "receive-stones":
                
                if sequence_num != 1 or len(i) != 2 or i[1] not in ["B", "W"]:
                    
                    reportInvalid(s)
                    break
                P.set_stone(i[1])
                
                with open('go-player.config') as json_file:
                    go_player_config = json.load(json_file)
                P.set_n(go_player_config['depth'])
                s.send(pickle.dumps(""))
            elif i[0] == "make-a-move":
                if sequence_num <= 1 or len(i) != 2 or (len(i[1]) not in {1,2,3}):
                    
                    reportInvalid(s)
                    break
                break_flag = 0
                for a in i[1]:
                    if len(a) != 19:
                        reportInvalid(s)
                        break_flag = 1
                        break
                    for j in a:
                        if len(j) != 19:
                            reportInvalid(s)
                            break_flag = 1
                            break
                        for k in j:
                            if k not in ["B","W"," "]:
                                reportInvalid(s)
                                break_flag = 1
                                break
                    if break_flag: break
                if break_flag:
                    break
                
                result = tuple_to_string(P.make_move(i[1]))
                s.send(pickle.dumps(result))
            else:
                reportInvalid(s)
                
                break
            sequence_num += 1
    except EOFError:
        pass
    s.shutdown(1)
    s.close()

if __name__ == "__main__":
    main()
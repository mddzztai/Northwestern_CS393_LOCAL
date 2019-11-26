from default_player import *
from global_variables import GET_PLAYERS_CONFIG
from referee import *
import socket
import sys

def main():
	#connect the remote players
	remote_player = dict()
	#set up the socket
	add, p = GET_PLAYERS_CONFIG()
	#load player() class
	spec = importlib.util.spec_from_file_location("module.name", p)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(add)
	s.listen(5)
	
	for i in range(n):
		conn, _ = s.accept()
		rm = foo.remote_player(conn)
		name = rm.register()
		remote_player[name] = rm
	
	s.close()


	if match_type == '-league':
		pass
	else:
		pass
	
# FOR ROUND ROBIN
# for loop outer(on player array)

# {
# 	for loop inner(on player array)
# 	{
# 		// Check that inner and  outer player are not the same

# 		// get the winner between each pair

# 		//update the result array according to it(result is the two dimesional array of pair(int,string)) where int =0,1 depending on who won
# 		string is the name of the opposition player

# 		//if a player is cheating add it to a new cheating array. Also replace this player with a new player in the intial 
# 		player array(player array is an array of players which we are iterating the for loop on)




# 	}

# }

# FOR KNOCKOUT

# initialize a new array outside to store winners called winner array outside the for loop

# for loop(on player array)

# {
# 	//maintain 2 indexes , i for the beginning of the array, j for the end, so we will do i++ , j--

# 	// get the winner between each pair(i,j)

# 	//add the winner to winner array

# 	// we will have a 1 dimesional int score array to store the score intially intialized to 0

# 	// for all the winners increment the score by 1

# 	// if some losing player lost due to cheating put its score to 0 in the score array

# 	//if (i==j) then make player array same as the winner array so that the loop continues


# }

if __name__ == "__main__":
	if len(sys.argv) != 3:
		raise Exception('Wrong Number of Arguments')
	_, match_type, n = sys.argv
	if match_type not in ['-league', '-cup']:
		raise Exception('Do not support this game')
	if not n.isnumeric():
		raise Exception('Wrong type for the number of remote player')
	n = int(n)
	if n < 0 or n > 16:
		raise Exception('Wrong number of remote players')
	main()
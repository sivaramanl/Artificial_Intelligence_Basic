"""
Created on Sat Oct 13 22:01:07 2018

@author: SIVARAMAN LAKSHMIPATHY

Problem statement 15 puzzle problem IDA*
"""

import time
import os
try:
    #to calculate memory usage
    import psutil
except ImportError:
    print("Unable to import psutil. Will install psutil now.")
    os.system('sudo python -m pip install psutil')
import psutil
#list to hold the solution for 15 puzzle problem
soln_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
max_exec_time = 30 * 60 #in seconds
start_time = 0
heuristic_used = 1
nodes_expanded = 0

def validate_input_sequence(seq):
    if len(seq) != 16:
        print("The given input sequence does not fall within the applicable size limits. Please verify the input sequence.")
        return False
    elif 0 not in seq:
        print("The given input sequence does not contain the element 0. Please verify the input sequence.")
        return False
    elif all(item in soln_list for item in seq) == False:
        print("The input sequence contains items not supported in the puzzle. Please verify the input sequence.")
        return False
    else:
        seq_copy = seq.copy()
        for item in soln_list:
            if item in seq_copy:
                seq_copy.remove(item)
        if len(seq_copy) > 0:
            print("There are duplicate items in the input sequence. Please verify the input sequence.")
            return False
    return True
        
def is_soln(h_n):
    #check if the new h(n) equals 0
    return h_n == 0
    
def print_soln(moves, end_time):
    global nodes_expanded
    final_path = "".join(move for move in moves)
    #print the solution
    print("Moves:", final_path)
    print("Number of Nodes expanded:", nodes_expanded)
    print("Time taken:", (end_time - start_time) * 1000, "\bms")
    print("Memory used:", psutil.Process(os.getpid()).memory_info().rss * 0.001, "\bkb")
    
def get_actions(node):
    action_state_pairs = []
    
    #find location of 0
    locn_0 = node.index(0)
    
    #Based on the location of the item 0 (which is the only actionable item), define the available actions.
    
    if 3 <= locn_0 <= 16:
        #action UP
        node[locn_0], node[locn_0-4] = node[locn_0-4], node[locn_0]
        action_state_pairs += [['U', node.copy()]]
        node[locn_0], node[locn_0-4] = node[locn_0-4], node[locn_0]
        
    if 0 <= locn_0 <= 11:
        #action DOWN
        node[locn_0], node[locn_0+4] = node[locn_0+4], node[locn_0]
        action_state_pairs += [['D', node.copy()]]
        node[locn_0], node[locn_0+4] = node[locn_0+4], node[locn_0]
        
    if locn_0%4 != 0:
        #action LEFT
        node[locn_0], node[locn_0-1] = node[locn_0-1], node[locn_0]
        action_state_pairs += [['L', node.copy()]]
        node[locn_0], node[locn_0-1] = node[locn_0-1], node[locn_0]
        
    if (locn_0+1)%4 != 0:
        #action RIGHT
        node[locn_0], node[locn_0+1] = node[locn_0+1], node[locn_0]
        action_state_pairs += [['R', node.copy()]]
        node[locn_0], node[locn_0+1] = node[locn_0+1], node[locn_0]
        
    #action_state_pairs contains all the available actions and their resultant states as [action, resultant_state] pairs
    return action_state_pairs
    
def getLeastValue(listObj):
    #method to return the item with the least value in the list
    listObj.sort()
    return listObj[0]
    
def calculate_manhattan_distance(indx1, indx2):
    #calculate the manhattan distance between the actual position of the tile and the intended final position of the tile
    if indx1 == indx2:
        return 0
    return abs(indx1%4 - indx2%4) + abs(indx1//4 - indx2//4)
    
def heuristic_number_of_misplaced_tiles(seq):
    #calculate the number of misplaced tiles in the current state of the puzzle
    global soln_list
    misplaced_tiles = 0
    for item in seq:
        if item == 0:
            continue
        elif seq.index(item) != soln_list.index(item):
            misplaced_tiles += 1
    return misplaced_tiles
    
def heuristic_manhattan_distance(seq):
    #calculate the total manhattan distance for all the tiles in the puzzle
    global soln_list
    manhattan_distance = 0
    for item in seq:
        if item == 0:
            continue
        else:
            manhattan_distance += calculate_manhattan_distance(seq.index(item), soln_list.index(item))
    return manhattan_distance
    
def calculate_f_n(prev_cost, seq):
    #calculate the f(n) = g(n) + h(n) value for the current state of the puzzle
    #f(n) - estimated total cost
    #g(n) - cost to reach the current state
    #h(n) - heuristic cost to reach the goal state
    #Since there are two heuristic values, the heuristic to be used is decided based on the value of the global variable heuristic_used
    #heuristic_value = max(heuristic_manhattan_distance(seq), heuristic_number_of_misplaced_tiles(seq))
    global heuristic_used
    heuristic_value = -1
    if heuristic_used == 1:
        heuristic_value = heuristic_number_of_misplaced_tiles(seq)
    else:
        heuristic_value = heuristic_manhattan_distance(seq)
    return prev_cost + heuristic_value, heuristic_value
    
def puzzle15_dlastar(seq, f_n_limit):
    #invoke the recursive value limited search with initial set of moves as an empty list
    return puzzle15_recursive_dlastar(seq, 0, f_n_limit, [], [])
    
def puzzle15_recursive_dlastar(current_node, prev_cost, f_n_limit, moves, f_n_exceeding_limit):
    global nodes_expanded
    global start_time
    time_elapsed = time.time() - start_time
    if time_elapsed > max_exec_time:
        #maximum execution time exhausted
        return "timeout", []
    f_n, h_n = calculate_f_n(prev_cost, current_node)
    if is_soln(h_n):
        #current node is solution. Print the solution and return
        print_soln(moves, time.time())
        return "success", f_n_exceeding_limit
    elif f_n > f_n_limit:
        f_n_exceeding_limit.append(f_n)
        return "cutoff", f_n_exceeding_limit
    else:
        nodes_expanded += 1
        cutoff_occurred = False
        action_state_pairs = get_actions(current_node)
        #iterate all actions and the resultant search states and check for solution state
        for action_state in action_state_pairs:
            new_state = action_state[1]
            temp_moves = moves.copy()
            temp_moves.append(action_state[0])
            #invoke the recursive call to perform f_n limited search on the child node
            status, f_n_exceeding_limit = puzzle15_recursive_dlastar(new_state, prev_cost+1, f_n_limit, temp_moves, f_n_exceeding_limit)
            if status == "cutoff":
                cutoff_occurred = True
            elif status != "failure":
                return status, f_n_exceeding_limit
        if cutoff_occurred == True:
            return status, f_n_exceeding_limit
        else:
            return "failure", f_n_exceeding_limit
    
def puzzle15_idastar(seq):
    f_n, h_n = calculate_f_n(0, seq)
    #invoke the depth limited search with incremental f(n) values
    while True:
        status, new_f_n_values_greater_than_f_n = puzzle15_dlastar(seq, f_n)
        if status == "success":
            return
        elif status == "failure":
            print("No solution exists.")
            return
        elif status == "timeout":
            print("Solution cannot be found since the maximum execution time has been exceeded.")
            return
        f_n = getLeastValue(new_f_n_values_greater_than_f_n)
    return
    
def main():
    #Step 1: fetch the input sequence from the user
    print("Please enter the input sequence: ")
    ip_seq = input().strip()
    global start_time 
    start_time = time.time()
    ip_seq_clean = []
    
    #Step 2: clean the input sequence
    try:
        ip_seq_clean = list(map(int, ip_seq.split(' ')))
    except ValueError:
        print("Please enter correct input.")
        exit()
    if validate_input_sequence(ip_seq_clean) == False:
        exit()
    #Step 3: invoke the method to calculate the solution for the input sequence, if any
    global heuristic_used
    global nodes_expanded
    #Heuristic 1: Number of misplaced tiles
    print("Searching for solution using Heuristic 1: Number of misplaced tiles")
    puzzle15_idastar(ip_seq_clean)
    #Heuristic 2: Manhattan distance
    heuristic_used = 2
    nodes_expanded = 0
    start_time = time.time()
    print("\nSearching for solution using Heuristic 2: Manhattan distance")
    puzzle15_idastar(ip_seq_clean)

if __name__ == '__main__':
    main()

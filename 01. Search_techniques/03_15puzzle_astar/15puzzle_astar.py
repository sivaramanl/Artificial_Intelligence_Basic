"""
Created on Wed Oct 10 10:05:19 2018

@author: SIVARAMAN LAKSHMIPATHY

Problem statement 15 puzzle problem A*
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
step_cost = 1
heuristic_used = 1

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

def get_path_from_root(branch_seq, index):
    #Fetch the path from the given node to its immediate parent and continue recursively.
    soln_node = branch_seq[index]
    if soln_node[1] == -1:
        return ''
    final_path = soln_node[0] + get_path_from_root(branch_seq, soln_node[1])
    return final_path

def print_soln(branch_seq, nodes_expanded, end_time):
    final_path = get_path_from_root(branch_seq, len(branch_seq)-1)
    #print the solution
    #The final_path is generated from the solution state to the initial state. Have to reverse the path.
    print("Moves:", final_path[::-1])
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
    
def add_to_frontier(frontier, node, cost, f_n):
    #construct and append the new node to the frontier
    frontier.append([node, cost, f_n])
    
def getNextLeastCostNode(frontier, explored):
    #identify and return the state in the search space which satisfies both the following conditions
    #a) is not yet explored
    #b) has the least f(n) value
    #the index of the item is also returned in order to remove it from the frontier
    local_f_n = -1
    indx = -1
    local_item = []
    local_indx = -1
    for item in frontier:
        indx += 1
        if indx in explored:
            continue
        item_f_n = item[2]
        if local_f_n == -1 or item_f_n < local_f_n:
            local_f_n = item_f_n
            local_item = item
            local_indx = indx
    return local_item, local_indx

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
    
def check_if_exists(it, frontier):
    #method to check if the state has already occurred in the frontier
    for item in frontier:
        if it == item[0]:
            return True
    return False

def puzzle15_astar(seq):
    nodes_expanded = 0
    current_node = seq
    #branch_seq holds the [action, parent_node_index] for each state explored, identified by the order (index) of exploration
    branch_seq = [['-', -1]]
    #add the initial state to the frontier
    frontier = []
    initial_state_f_n = calculate_f_n(0, current_node)
    if is_soln(initial_state_f_n[1]):
        #initial state is solution. Print the solution and return.
        print_soln(branch_seq, nodes_expanded, time.time())
        return
    add_to_frontier(frontier, current_node, 0, initial_state_f_n)
    #declare explored as an empty list
    explored = []
    current_max_cost = 0
    while True:
        if len(frontier) == 0:
            #The frontier has been exhausted but there are no solutions to the puzzle.
            print("Solution cannot be found.")
            return
        #pop the element from the frontier queue with the least f(n) value
        current_node, current_node_indx = getNextLeastCostNode(frontier, explored)
        #add the index of current node to explored list
        explored.append(current_node_indx)
        action_state_pairs = get_actions(current_node[0])
        nodes_expanded += 1
        #iterate all actions and the resultant search states and check for solution state
        for action_state in action_state_pairs:
            new_state = action_state[1]
            if check_if_exists(new_state, frontier) == False:
                new_action = action_state[0]
                branch_seq += [[new_action, current_node_indx]]
                #calculate the f(n) value for the new state
                new_f_n, new_h_n = calculate_f_n(current_node[1]+1, new_state)
                add_to_frontier(frontier, new_state, current_node[1]+1, new_f_n)
                if is_soln(new_h_n):
                    print(new_h_n)
                    print_soln(branch_seq, nodes_expanded, time.time())
                    return
        time_elapsed = time.time() - start_time
        if time_elapsed > max_exec_time:
            #maximum execution time exhausted
            print("Solution cannot be found since the maximum execution time has been exceeded.")
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
    #Heuristic 1: Number of misplaced tiles
    print("Searching for solution using Heuristic 1: Number of misplaced tiles")
    puzzle15_astar(ip_seq_clean)
    #Heuristic 2: Manhattan distance
    heuristic_used = 2
    start_time = time.time()
    print("\nSearching for solution using Heuristic 2: Manhattan distance")
    puzzle15_astar(ip_seq_clean)

if __name__ == '__main__':
    main()

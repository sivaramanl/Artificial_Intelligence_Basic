"""
Created on Thu Sep 27 03:05:19 2018

@author: SIVARAMAN LAKSHMIPATHY

Problem statement 15 puzzle problem BFS
"""

import time
import os
import psutil
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
        
def is_soln(seq):
    #check if the generated sequence matches the solution sequence
    return soln_list == seq

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
        

def puzzle15_bfs(seq):
    nodes_expanded = 0
    current_node = seq
    frontier_iterator = 0
    #branch_seq holds the [action, parent_node_index] for each state explored, identified by the order (index) of exploration
    branch_seq = [['-', -1]]
    if is_soln(current_node):
        #initial state is solution. Print the solution and return.
        print_soln(branch_seq, nodes_expanded, time.time())
        return
    #add the initial state to the frontier
    frontier = [current_node]
    #declare explored as an empty list
    explored = []
    while True:
        if len(frontier) == 0:
            #The frontier has been exhausted but there are no solutions to the puzzle.
            print("Solution cannot be found.")
            return
        #pop the element from the frontier queue
        current_node = frontier[0]
        frontier = frontier[1:]
        #increment iterator tracking the index of the element in the queue
        frontier_iterator += 1
        #check for repeated state
        if current_node in explored:
            continue
        #add to explored list
        explored += current_node
        action_state_pairs = get_actions(current_node)
        nodes_expanded += 1
        #iterate all actions and the resultant search states and check for solution state
        for action_state in action_state_pairs:
            new_state = action_state[1]
            if new_state not in frontier and new_state not in explored:
                frontier += [new_state]
                new_action = action_state[0]
                branch_seq += [[new_action, frontier_iterator-1]]
                if is_soln(new_state):
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
    ip_seq = input()
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
    puzzle15_bfs(ip_seq_clean)

if __name__ == '__main__':
    main()

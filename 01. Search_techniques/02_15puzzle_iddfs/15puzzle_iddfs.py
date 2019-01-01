# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 00:14:00 2018

@author: SIVARAMAN LAKSHMIPATHY

Problem statement 15 puzzle problem IDDFS

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
nodes_expanded = 0
frontier_iterator = 0

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

def puzzle15_dls(seq, depth):
    #invoke the recursive depth limited search with initial set of moves as an empty list
    return puzzle15_recursive_dls(seq, depth, [])

def puzzle15_recursive_dls(current_node, limit, moves):
    global nodes_expanded
    global start_time
    time_elapsed = time.time() - start_time
    if time_elapsed > max_exec_time:
            #maximum execution time exhausted
            return "timeout"
    if is_soln(current_node):
        #initial state is solution. Print the solution and return.
        print_soln(moves, time.time())
        return "success"
    elif limit == 0:
        return "cutoff"
    else:
        nodes_expanded += 1
        cutoff_occurred = False
        action_state_pairs = get_actions(current_node)
        #iterate all actions and the resultant search states and check for solution state
        for action_state in action_state_pairs:
            new_state = action_state[1]
            temp_moves = moves.copy()
            temp_moves.append(action_state[0])
            #invoke the recursive call to perform dls on the child node
            status = puzzle15_recursive_dls(new_state, limit-1, temp_moves)
            if status == "cutoff":
                cutoff_occurred = True
            elif status != "failure":
                return status
        if cutoff_occurred == True:
            return status
        else:
            return "failure"

def puzzle15_iddfs(seq):
    depth = 0
    #invoke the depth limited search with incremental depths
    while True:
        status = puzzle15_dls(seq, depth)
        if status == "success":
            return
        elif status == "failure":
            print("No solution exists.")
            return
        elif status == "timeout":
            print("Solution cannot be found since the maximum execution time has been exceeded.")
            return
        depth += 1
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
    puzzle15_iddfs(ip_seq_clean)

if __name__ == '__main__':
    main()

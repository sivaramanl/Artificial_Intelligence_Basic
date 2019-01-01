# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 19:22:35 2018

@author: Sivaraman Lakshmipathy

MDP problem for generic grid world

Example 4 x 3 grid world
   --------------------
3 |    |    |    | +1 |
   --------------------
2 |    |xxxx|    | -1 |
   --------------------
1 |    |    |    |    |
   --------------------
    1    2    3     4
"""

#class to hold each node in the grid world
class mdp_node:
    row_val = -1
    col_val = -1
    is_unreachable_state = False
    is_terminal_state = False
    reward = 0
    
    def __init__(self, i, j, is_unreachable_state, is_terminal_state, reward):
        self.row_val = j
        self.col_val = i
        self.is_unreachable_state = is_unreachable_state
        self.is_terminal_state = is_terminal_state
        self.reward = reward
        
    #method to calculate the transition model for the node
    def calculate_transition_model(self, action, mov_prob, mdp_obj, utility_list):
        transition_val = 0
        for mov in mov_prob:
            if mov_prob[mov] > 0:
                i, j = getNextLocForAction(self.row_val, self.col_val, action, mov, mdp_obj)
                next_indx = (i * mdp_obj.columnsize) + j
                transition_val += (mov_prob[mov] * utility_list[next_indx])
        return transition_val
    
#class holding the grid world configurations
class mdp:
    rowsize = None
    columnsize = None
    mdp_nodes = []
    action_prob_mapping = {}#{'U' : 0.8, 'L' : 0.1, 'D' : 0, 'R' : 0.1}
    state_unreachable_val = []#[False, False, False, False, False, True, False, False, False, False, False, False]
    state_terminal_val = []#[False, False, False, False, False, False, False, True, False, False, False, True]
    reward = []
    gamma_discount_val = None
    
    def __init__(self, rowsize, columnsize, unreachable_states_location, terminal_states_desc, reward, transition_probabilities, gamma):
        self.rowsize = rowsize
        self.columnsize = columnsize
        self.state_unreachable_val = [False for i in range(self.rowsize * self.columnsize)]
        self.state_terminal_val = [False for i in range(self.rowsize * self.columnsize)]
        self.reward = [reward for i in range(self.rowsize * self.columnsize)]
        for action in transition_probabilities:
            self.action_prob_mapping[action] = transition_probabilities[action]
        self.gamma_discount_val = gamma
        for entry in unreachable_states_location:
            indx = (self.columnsize*(entry[1]-1)) + entry[0]-1
            self.reward[indx] = None
            self.state_unreachable_val[indx] = True
        for entry in terminal_states_desc:
            indx = (self.columnsize*(entry[1]-1)) + entry[0]-1
            self.state_terminal_val[indx] = True
            self.reward[indx] = entry[2]
        for j in range(self.rowsize):
            for i in range(self.columnsize):
                indx = (self.columnsize*j) + i
                self.mdp_nodes.append(mdp_node(i, j, self.state_unreachable_val[indx], self.state_terminal_val[indx], self.reward[indx]))

#method to get actual direction of movement for given action and probable direction of movement
def getNextLocForAction(row_val, col_val, action, mov, mdp_obj):
    actual_action = action #mov = 'U'
    old_row_val = row_val
    old_col_val = col_val
    if mov == 'L':
        if action == 'U':
            actual_action = 'L'
        elif action == 'L':
            actual_action = 'D'
        elif action == 'R':
            actual_action = 'U'
        elif action == 'D':
            actual_action = 'R'
    elif mov == 'R':
        if action == 'U':
            actual_action = 'R'
        elif action == 'L':
            actual_action = 'U'
        elif action == 'R':
            actual_action = 'D'
        elif action == 'D':
            actual_action = 'L'
    elif mov == 'D':
        if action == 'U':
            actual_action = 'D'
        elif action == 'L':
            actual_action = 'R'
        elif action == 'R':
            actual_action = 'L'
        else:
            actual_action = 'U'
            
    if actual_action == 'U':
        row_val = row_val+1
    elif actual_action == 'R':
        col_val = col_val+1
    elif actual_action == 'L':
        col_val = col_val-1
    else:
        row_val = row_val-1
    
    if row_val < 0 or col_val < 0 or row_val >= mdp_obj.rowsize or col_val >= mdp_obj.columnsize:
        return old_row_val, old_col_val
    new_indx = (row_val * mdp_obj.columnsize) + col_val
    if mdp_obj.mdp_nodes[new_indx].is_unreachable_state:
        return old_row_val, old_col_val
    return row_val, col_val

#method to print the utility values to the standard output and a text file
def print_utility_values(mdp_obj, utility_list, iter_count = None):
    output_str_final = []
    output_str = ""
    i = 0
    for state in mdp_obj.mdp_nodes:
            indx = (state.row_val * mdp_obj.columnsize) + state.col_val
            if not utility_list == None:
                output_str += str(utility_list[indx]) + "\t"
            else:
                if state.is_unreachable_state:
                    output_str += "None\t"
                else:
                    output_str += "0\t"
            i = i+1
            if(i % mdp_obj.columnsize == 0):
                output_str_final.append(output_str)
                output_str = ""
    if not iter_count == None:
        output_str = "\nIteration " + str(iter_count) + ":"
        output_str_final.append(output_str)
        output_str = ""
    output_str_final = list(reversed(output_str_final))
    for entry in output_str_final:
        print(entry)
        
    try:
        output_file = "mdp_value_iteration_op.txt"
        endline = "\n"
        if iter_count == 0:
            file_obj = open(output_file, "w")
        else:
            file_obj = open(output_file, "a")
        if iter_count == None:
            file_obj.write("\nFinal utility values:")
            file_obj.write(endline)
        for entry in output_str_final:
            file_obj.write(entry)
            file_obj.write(endline)
        file_obj.close()
    except:
        print("Error while printing output to output file.")
            
#method to get the maximum transition value for a given state
def getMaxTransitionVal(state, mdp_obj, U):
    transition_model_vals = []
    for action in mdp_obj.action_prob_mapping:
        transition_model_vals.append(state.calculate_transition_model(action, mdp_obj.action_prob_mapping, mdp_obj, U))
    return max(transition_model_vals)
    
#method to perform value iteration until convergence
def value_iteration(mdp_obj, epsilon):
    U = [0 for i in range(mdp_obj.rowsize*mdp_obj.columnsize)]
    U_prime = [0 for i in range(mdp_obj.rowsize*mdp_obj.columnsize)]
    
    iter_count = 0
    while True:
        U = U_prime.copy()
        delta = 0
        iter_count += 1
        for state in mdp_obj.mdp_nodes:
            indx = (state.row_val * mdp_obj.columnsize) + state.col_val
            if state.is_terminal_state or state.is_unreachable_state:
                U_prime[indx] = state.reward
                continue
            U_prime[indx] = state.reward + mdp_obj.gamma_discount_val * getMaxTransitionVal(state, mdp_obj, U_prime)
            abs_diff = abs(U_prime[indx] - U[indx])
            if (abs_diff) > delta:
                delta = abs_diff
        print_utility_values(mdp_obj, U_prime, iter_count)
        margin = epsilon * (1 - mdp_obj.gamma_discount_val) / mdp_obj.gamma_discount_val
        if delta > margin:
            continue
        break
    return U
    
#method to read the input file and convert to the required format in order to configure the grid world
def read_file_input(ip_file):
    file_obj = open(ip_file, "r")
    columnsize = -1
    rowsize = -1
    unreachable_states_location = [] #list containing location of unreachable states
    terminal_states_desc = [] #list containing location of terminal states along with the rewards
    reward = 0 #reward value for non-terminal states
    transition_probabilities = {'U': 0.0, 'L': 0.0, 'R': 0.0, 'D': 0.0}
    gamma = 1
    epsilon = 0
    for line in file_obj:
        if "#" not in line:
            if "size" in line:
                sizeval = line.split(":")[1].strip()
                columnsize = int(sizeval.split(" ")[0].strip())
                rowsize = int(sizeval.split(" ")[1].strip())
            elif "wall" in line:
                location_val = line.split(":")[1].strip()
                locations = location_val.split(",")
                for location in locations:
                    location = location.strip()
                    loc = []
                    loc.append(int(location.split(" ")[0].strip()))
                    loc.append(int(location.split(" ")[1].strip()))
                    unreachable_states_location.append(loc)
            elif "terminal_states" in line:
                terminal_val = line.split(":")[1].strip()
                terminals = terminal_val.split(",")
                for terminal in terminals:
                    terminal = terminal.strip()
                    ter = []
                    ter.append(int(terminal.split(" ")[0].strip()))
                    ter.append(int(terminal.split(" ")[1].strip()))
                    ter.append(int(terminal.split(" ")[2].strip()))
                    terminal_states_desc.append(ter)
            elif "reward" in line:
                reward = float(line.split(":")[1].strip())
            elif "transition_probabilities" in line:
                transition_val = line.split(":")[1].strip()
                transitions = transition_val.split(" ")
                transition_probabilities['U'] = float(transitions[0].strip())
                transition_probabilities['L'] = float(transitions[1].strip())
                transition_probabilities['R'] = float(transitions[2].strip())
                transition_probabilities['D'] = float(transitions[3].strip())
            elif "gamma" in line:
                gamma = float(line.split(":")[1].strip())
            elif "epsilon" in line:
                epsilon = float(line.split(":")[1].strip())
    return rowsize, columnsize, unreachable_states_location, terminal_states_desc, reward, transition_probabilities, gamma, epsilon
          
def main():
    input_file = "mdp_value_iteration_ip.txt"
    epsilon = 0.001
    try:
        rowsize, columnsize, unreachable_states_location, terminal_states_desc, reward, transition_probabilities, gamma, epsilon = read_file_input(input_file)
        mdp_obj = mdp(rowsize, columnsize, unreachable_states_location, terminal_states_desc, reward, transition_probabilities, gamma)
    except:
        print("Error while initializing the MDP.")
        return
    print("Performing value iteration")
    print_utility_values(mdp_obj, None, 0)
    utility_vals = value_iteration(mdp_obj, epsilon)
    print("\nFinal utility values:")
    print_utility_values(mdp_obj, utility_vals)
    
if __name__ == '__main__':
    main()

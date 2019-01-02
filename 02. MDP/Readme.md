MDP (Markov decision process) problem for generic grid world
---------------------
1. The source code for identifying the utility values of each state in a generic grid world problem has been implemented in Python (Python version 3.6.5)
2. The name of the source code file is mdp_value_iteration.py
3. The input for the problem can be provided in the mpd_value_iteration_ip.txt file. The output will be printed to the standard console and also recorded in mdp_value_iteration_op.txt file which will be generated on executing the source code. 
4. Execute the file.
> python mdp_value_iteration.py

Configuring the input file
--------------------------
1. A sample grid world will be shown in the input file.
2. Please enter the size of the grid world as number of columns and number of rows. For example, for a 4 x 3 world, the number of columns is 4 and number of rows is 3 corresponding to the 'size' entry.
3. Enter the location of all the walls as the coordinates of their locations (column, row) seperated by a comma corresponding to the 'walls' entry.
4. Enter the list of the terminal states and their rewards as triplets (column, row, reward) separated by a comma corresponding to the 'terminal_states' entry.
5. Enter the reward value for non-terminal states corresponding to the 'reward' entry.
6. Enter the transition probabilities as a four-valued tuple for the four directions (Forwards, Left, Right, Backward) corresponding to the 'transition_probabilities' entry.
7. Enter the gamma discount value corresponding to the 'gamma' entry.
8. Enter the epsilon value corresponding to the 'epsilon' entry.
Note: Please do not change the labels since the values are required for the source code to run successfully.

Note: Sample input and output files are included in the directory.

Algorithm source: Artificial Intelligence A modern approach 3rd edition S. Russell and P.Norvig

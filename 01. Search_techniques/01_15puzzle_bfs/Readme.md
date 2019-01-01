15 puzzle - BFS (Breadth first search)
Readme
---------------------
1. The source code for the 15 puzzle problem has been implemented in Python (Python version 3.6.5)
2. The name of the source code file is 15puzzle_bfs.py
3. Execute the file.
> python 15puzzle_bfs.py
4. Please enter the input sequence when prompted.
5. The source code utilizes 'psutil' module to calculate the memory usage of the execution. If the module is unavailable, the module will be downloaded and installed automatically. If it encounters any errors, kindly execute the file as a super user.
6. The maximum execution time has been fixed at 30 minutes. If the solution to the puzzle is not identified within 30 minutes, the execution will stop with an error message.
7. The solution, if found, will be printed as the list of moves required to reach the goal state from the initial state.

Algorithm source: Artificial Intelligence A modern approach 3rd edition S. Russell and P.Norvig

Example input:
2 3 4 0 1 5 7 8 9 6 10 12 13 14 11 15
Output for example input:
Moves: LLLDRDRDR
Number of Nodes expanded: 1734
Time taken: 987.4017238616943ms
Memory used: 17215.488kb

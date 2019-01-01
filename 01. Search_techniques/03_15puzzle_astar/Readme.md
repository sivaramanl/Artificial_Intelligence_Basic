15 puzzle - A*
Readme
---------------------
1. The source code for the 15 puzzle problem has been implemented in Python (Python version 3.6.5)
2. The name of the source code file is 15puzzle_astar.py
3. Execute the file.
> python 15puzzle_astar.py
4. Please enter the input sequence when prompted.
5. The source code utilizes 'psutil' module to calculate the memory usage of the execution. If the module is unavailable, the module will be downloaded and installed automatically. If it encounters any errors, kindly execute the file as a super user.
6. The maximum execution time has been fixed at 30 minutes. If the solution to the puzzle is not identified within 30 minutes, the execution will stop with an error message.
7. The solution, if found, will be printed as the list of moves required to reach the goal state from the initial state. Two solutions, one for each heuristic, will be printed.

Algorithm source: Artificial Intelligence A modern approach 3rd edition S. Russell and P.Norvig

Example input:
2 3 4 0 1 5 7 8 9 6 10 12 13 14 11 15
Output for example input:
Searching for solution using Heuristic 1: Number of misplaced tiles
Moves: LLLDRDRDR
Number of Nodes expanded: 9
Time taken: 0.9970664978027344ms
Memory used: 14307.328kb

Searching for solution using Heuristic 2: Manhattan distance
Moves: LLLDRDRDR
Number of Nodes expanded: 9
Time taken: 0.0ms
Memory used: 14311.424kb
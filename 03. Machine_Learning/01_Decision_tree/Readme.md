Decision Tree implementation for binary classification
---------------------
1. The source code for generating the decision tree for binary classification from the given dataset has been implemented in Python (Python version 3.6.5)
2. The name of the source code file is decision_tree.py
3. The input file name is "restaurant.csv" by default, when no command line arguments are provided.
> python decision_tree.py
4. If a different file name is to be used, it can be provided as a command line argument.
> python decision_tree.py new_file.csv
5. Please note that the first line of the CSV file IS NOT considered to be the header by default, i.e., the source code assumes that there are no headers and hence prints the decision tree with the attributes named corresponding to the column numbers in the CSV file.
If the first line of the input file is to be considered as header, please include the "--header" option as the second command line argument.
> python decision_tree.py new_file.csv --header
This does not work without the first parameter being the file name. Thus, if the file is named "restaurant.csv" and contains headers, the source code is to be executed as follows.
> python decision_tree.py restaurant.csv --header
6. The decision tree will be printed in the command prompt.

Algorithm source: Artificial Intelligence A modern approach 3rd edition S. Russell and P.Norvig

Output for "restaurant.csv":
Please refer to Decision_tree_output.PNG

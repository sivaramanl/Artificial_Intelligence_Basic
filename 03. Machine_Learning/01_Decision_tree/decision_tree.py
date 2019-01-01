# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 22:24:58 2018

@author: Sivaraman Lakshmipathy

Decision Tree implementation for binary classification
"""

import numpy as np
import math
import sys

#class to hold distinct nodes in the decision tree
class tree_node:
    attribute = None
    branches = None
    
    def __init__(self, attr_val):
        self.attribute = attr_val
        self.branches = {}
        
    def addBranch(self, action, tree_node):
        self.branches[action] = tree_node
        
#method to print the decision tree
def printTree(tree_node, header=[], level=0):
    if isinstance(tree_node, str):
        print(tree_node)
        return
    if len(header) > 0 and tree_node.attribute-1 < len(header):
        print(header[tree_node.attribute-1])
    else:
        print("Attribute:", tree_node.attribute)
    for entry in tree_node.branches:
        for i in range(level):
            print("\t", end="")
        print("--", entry, "? ", end="")
        printTree(tree_node.branches[entry], header, level+2)
    
#method to read the examples to be processed from the given input file
def readExamplesFromFile(fileName, headerAvailable=False, delimiter=","):
    examples = []
    header = []
    
    file_obj = open(fileName, "r")
    if headerAvailable:
        headerLine = file_obj.readline()
        header = headerLine.split(",")
        for i in range(len(header)):
            header[i] = header[i].strip()
    for line in file_obj:
        tokens = line.split(",")
        for i in range(len(tokens)):
            tokens[i] = tokens[i].strip()
        examples.append(tokens)
    return np.array(examples), header

#method to identify the mode output class
def most_freq_target(target, examples):
    unique_vals = np.unique(examples[:, target])
    unique_vals[::-1].sort()
    max_val_len = 0
    max_val = None
    for val in unique_vals:
        val_len = len(np.where((examples[:,target]==val) == True)[0])
        if val_len > max_val_len:
            max_val_len = val_len
            max_val = val
    return max_val, max_val_len

#method to calculate the entropy
def get_entropy(p_val):
    if p_val == 0 or p_val == 1:
        return 0
    return (-1 * p_val) * math.log(p_val, 2) + (-1 * (1 - p_val)) * math.log((1 - p_val), 2)

#method to identify the feature to split on based on Information Gain
def getMostImportantAttribute(examples, attributes, target):
    examples_len = len(examples)
    unique_target_vals = np.unique(examples[:, target])
    entropy_examples = 0
    entropy_attributes = []
    for val in unique_target_vals:
        val_len = len(np.where((examples[:,target]==val) == True)[0])
        p_val = val_len/examples_len
        entropy_examples += (-1 * p_val) * math.log(p_val, 2)
    for attr in attributes:
        if attr == -1:
            entropy_attributes.append(-1)
            continue
        unique_attrs = np.unique(examples[:, attr])
        attr_entropy = 0
        for unique_attr in unique_attrs:
            rows_for_unique_attr = examples[np.where((examples[:,attr]==unique_attr) == True)]
            unique_attr_len = len(rows_for_unique_attr)
            p_val = len(np.where((rows_for_unique_attr[:, target]==unique_target_vals[0])==True)[0])/unique_attr_len
            attr_entropy += (unique_attr_len / examples_len) * get_entropy(p_val)
        entropy_attributes.append(entropy_examples - attr_entropy)
    return entropy_attributes.index(max(entropy_attributes))

#method to construct the decision tree from the given dataset
def decision_tree_learning(examples, attributes, target, parent_examples):
    if len(examples) == 0:
        return most_freq_target(target, parent_examples)[0]
    elif len(attributes) == 0:
        return most_freq_target(target, examples)[0]
    else:
        most_freq_target_val = most_freq_target(target, examples)
        if len(examples) == most_freq_target_val[1]:
            return most_freq_target_val[0]
        else:
            A = getMostImportantAttribute(examples, attributes, target)
            tree = tree_node(A+1)
            sub_attributes = attributes.copy()
            sub_attributes[attributes.index(A)] = -1
            unique_vals_for_A = np.unique(parent_examples[:, A])
            for val in unique_vals_for_A:
                sub_examples = []
                sub_examples = examples[np.where((examples[:,A]==val) == True)]
                sub_tree = decision_tree_learning(sub_examples, sub_attributes, target, examples)
                tree.addBranch(val, sub_tree)
            return tree
            
def main():
    fileName = "restaurant.csv" #default file name
    headerAvailable = False
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--header":
        headerAvailable = True
    examples, header = readExamplesFromFile(fileName, headerAvailable)
    target_col = len(examples[0]) - 1
    attributes = []
    for i in range(len(examples[0]) - 1):
        attributes.append(i)
    print("Decision Tree\n")
    decision_tree = decision_tree_learning(examples, attributes, target_col, examples)
    if headerAvailable:
        printTree(decision_tree, header)
    else:
        printTree(decision_tree)
            
if __name__ == '__main__':
    main()

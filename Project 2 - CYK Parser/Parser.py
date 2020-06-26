## Mark Koszykowski
## ECE467 - Natural Language Processing
## Project 2 - CYK Parser

import string

# Function to import document of rules and store them in a list of lists
def import_rules(CNF_rules=0):

    # Opening of file with CNF rules
    CNF_file = open(CNF_rules, 'r')
    CNF_file_lines = CNF_file.read().splitlines()

    rules = []

    print("\n...Importing Chomsky Normal Form Rules...\n")

    # Loop through lines in the file to store rules into a list of lists
    for line in CNF_file_lines:
        line_rule = []

        line_info = line.split()

        first = line_info[0]
        second = line_info[2]

        # Add the elements of the rules to a list
        line_rule.append(first)
        line_rule.append(second)

        # If the line contains two non-terminals, add it to the list
        if(len(line_info) == 4):
            third = line_info[3]

            line_rule.append(third)

        # Add this list to the list of lists
        rules.append(line_rule)

    return rules

class Node:
    def __init__(self, symbol, r1, r2 = None):
        self.symbol = symbol
        self.r1 = r1
        self.r2 = r2

# Function to print elements of parse list
def print_parse(node):
    if node.r2 == None:
        string = "[" + node.symbol + " '" + node.r1 + "']"
        return string
    else:
        string = "[" + node.symbol + " " + print_parse(node.r1) + " " + print_parse(node.r2) + "]"
        return string

# Function to parse sentence
def sentence_parse(sentence = 0, CNF_rules = 0):

    # Removes all capital letters and punctuation
    sentence = sentence.translate(str.maketrans('', '', string.punctuation)).lower()

    # Splits up sentence into its words
    words = sentence.split()

    length = len(words)

    # Creates a triangular CYK matrix
    CYK_table = [[[] for i in range(length - j)] for j in range(length)]

    # Fills in the first column of the matrix
    index = 0
    for word in words:
        for rule in CNF_rules:
            if word == rule[1]:
                CYK_table[0][index].append(Node(rule[0], word))
        index += 1

    # Fills in the rest of the columns of the CYK matrix
    for words in range(2, length+1):
        for cell in range(0, length-words+1):
            for left_size in range(1, words):
                right_size = words - left_size

                left_cell = CYK_table[left_size-1][cell]
                right_cell = CYK_table[right_size-1][cell+left_size]

                for rule in CNF_rules:
                    left_nodes = []
                    for i in left_cell:
                        if i.symbol == rule[1]:
                            left_nodes.append(i)

                    if left_nodes:
                        right_nodes = []
                        for i in right_cell:
                            if len(rule) == 3:
                                if i.symbol == rule[2]:
                                    right_nodes.append(i)

                        for l_node in left_nodes:
                            for r_node in right_nodes:
                                CYK_table[words-1][cell].append(Node(rule[0], l_node, r_node))

    # Every valid parse will begin with 'S'
    first_symbol = "S"

    # Puts all valid parses into a list
    parses = []
    for element in CYK_table[-1][0]:
        if element.symbol == first_symbol:
            parses.append(element)

    # If list is not empty, print it
    if parses:
        num_parses = 1
        for parse in parses:
            print("\nParse #" + str(num_parses) + ":")
            print(print_parse(parse))

            num_parses += 1

        print("\nThis sentence has " + str(num_parses-1) + " valid parses.\n\n")

    else:
        print("NO VALID PARSES.\n\n")

    return

# Asks user for inputted rules and sentence
CNF_file = input("Enter the name of the file with the rules in Chomsky Normal Form: ")
CNF_rules = []
CNF_rules = import_rules(CNF_file)
sentence = input("Enter a sentence to be parsed or type 'quit' to end program:\n")

# Continues to loop as long as sentence is not 'quit'
while sentence != "quit":

    sentence_parse(sentence, CNF_rules)
    sentence = input("Enter a sentence to be parsed or type 'quit' to end program:\n")
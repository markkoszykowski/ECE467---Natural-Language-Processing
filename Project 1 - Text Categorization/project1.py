## Mark Koszykowski
## ECE467 - Natural Language Processing
## Project 1 - Text Categorizer
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from math import log
import string

def text_categorize(train_input=0, test_input=0):

    #Declaration of additive smoothing constant
    k = .0725

    ##Training

    #Seperation of training documents
    train_list = open(train_input, 'r')
    train_list_lines = train_list.read().splitlines()

    #Declaration of dictionary that stores the specific token counts per category
    dic_word_cat = dict()

    #Declaration of dictionary that stores total token counts per category
    dic_tok_cat = dict()

    #Declaration of dictionary that counts the amount of files per category
    dic_files_cat = dict()

    #Loop through each line in training list
    for line in train_list_lines:

        #Division of line into a list of string information
        line_info = line.split()

        #Read the address of training document
        train_file = open(line_info[0], 'r')

        #Read the category of training document
        cat = line_info[1]

        #Tokenization of the training file
        train_tokenization = word_tokenize(train_file.read())

        #Keep count of categories being looped through
        if cat in dic_files_cat:
            dic_files_cat[cat] += 1.
        else:
            dic_files_cat[cat] = 1.

        #Loop through the words of the training document
        for token in train_tokenization:

            #Apply the stemmer to the token
            token = PorterStemmer().stem(token)

            #Count the number of times that this token appears in this category
            if (token, cat) in dic_word_cat:
                dic_word_cat[(token, cat)] += 1.
            else:
                dic_word_cat[(token, cat)] = 1.

            #Count the number of tokens that appear in this category
            if cat in dic_tok_cat:
                dic_tok_cat[cat] += 1.
            else:
                dic_tok_cat[cat] = 1.

    #Store the total number of training tiles
    num_train_files = sum(dic_files_cat.values())

    #Store category names into a list
    categories = dic_tok_cat.keys()

    ##Testing

    #Declaration of a list of predictions
    predictions = []

    #Seperation of testing documents
    test_list = open(test_input, 'r')
    test_list_lines = test_list.read().splitlines()

    #Loop through each line in testing list
    for line in test_list_lines:

        #Read the address of testing document
        test_file = open(line, 'r')

        #Tokenization of the testing file
        test_tokenization = word_tokenize(test_file.read())

        #Declaration of dictionary that stores tokens seen in testing document
        dic_tok_test = dict()

        #Declaration of dictionary that stores conditional log probabilities for testing document
        dic_log_prob = dict()

        #Calculates the vocabulary size of test document
        for test_token in test_tokenization:

            #Apply the stemmer to the token
            test_token = PorterStemmer().stem(test_token)

            if test_token in list(string.punctuation):
                pass
            elif test_token in dic_tok_test:
                dic_tok_test[test_token] += 1.
            else:
                dic_tok_test[test_token] = 1.

        vocab_size = len(dic_tok_test)

        for category in categories:

            #Initialization of conditional probability of article being in specific category
            total_cat_log_prob = 0.

            #Calculates the probability of category based on training set
            cat_prob = dic_files_cat[category] / num_train_files

            #Normalization coefficient for additive smoothing
            normalized = dic_tok_cat[category] + k * vocab_size

            #Calculates the conditional category probabilities
            for word, count in dic_tok_test.items():
                if (word, category) in dic_word_cat:
                    count_word_cat = dic_word_cat[(word, category)] + k
                else:
                    count_word_cat = k

                cat_log_prob = count * log(count_word_cat / normalized)
                total_cat_log_prob += cat_log_prob

            dic_log_prob[category] = total_cat_log_prob + log(cat_prob)

        #Determine a category decision based on highest probability
        decision = max(dic_log_prob, key = dic_log_prob.get)

        #Construct proper output notation
        str = line + ' ' + decision + '\n'
        predictions.append(str)

    #Ask user for name of output file
    test_output = input('Enter the name of the desired text categorized predictions file: ')

    #Write the final decision to the output file
    output_file = open(test_output, 'w')
    for line in predictions:
        output_file.write(line)

    output_file.close()

    return

train_input = input("Enter the name of the labeled list of training documents: ")
test_input = input("Enter the name of the list of testing documents to be categorized: ")

#Call to text categorization function
text_categorize(train_input, test_input)
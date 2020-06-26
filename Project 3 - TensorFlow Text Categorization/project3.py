## Mark Koszykowski
## ECE467 - Natural Language Processing
## Project 3 - Tensorflow Text Categorizer
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english'))

vocab_size = 4000
embedding_dim = 64
max_length = 1000
trunc_type = 'post'
padding_type = 'post'
oov_tok = '<OOV>'
training_portion = .8

def create_lists(train_input, test_input):

    train_list = open(train_input, 'r')
    train_list_lines = train_list.read().splitlines()

    articles = []
    labels = []

    for line in train_list_lines:

        line_info = line.split()

        labels.append(line_info[1])

        with open(line_info[0], 'r') as file:

            article = file.read().replace('\n','').replace('\t','').replace('  ', ' ').replace('``', '').replace("''", '').replace('"', '').strip()

            for word in STOPWORDS:
                token = ' ' + word + ' '
                article = article.replace(token, ' ')
                article = article.replace(' ', ' ')

            articles.append(article)

    test_list = open(test_input, 'r')
    test_list_lines = test_list.read().splitlines()

    test_articles = []

    for line in test_list_lines:
        with open(line, 'r') as file:
            article = file.read().replace('\n', '').replace('\t', '').replace('  ', ' ').replace('``', '').replace("''",
                                                                                                                   '').replace(
                '"', '').strip()

            for word in STOPWORDS:
                token = ' ' + word + ' '
                article = article.replace(token, ' ')
                article = article.replace(' ', ' ')

            test_articles.append(article)

    return articles, labels, test_articles

def train_and_cat(articles, labels, test_articles, vocab_size, embedding_dim, max_length, trunc_type, padding_type, oov_tok, training_portion):

    train_size = int(len(articles) * training_portion)

    train_articles = articles[0:train_size]
    train_labels = labels[0:train_size]

    tuning_articles = articles[train_size:]
    tuning_labels = labels[train_size:]

    tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
    tokenizer.fit_on_texts(train_articles)
    word_index = tokenizer.word_index

    train_sequences = tokenizer.texts_to_sequences(train_articles)
    train_padded = pad_sequences(train_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

    tuning_sequences = tokenizer.texts_to_sequences(tuning_articles)
    tuning_padded = pad_sequences(tuning_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

    label_tokenizer = Tokenizer()
    label_tokenizer.fit_on_texts(labels)

    output = {i: j for j, i in label_tokenizer.word_index.items()}


    training_label_seq = np.array(label_tokenizer.texts_to_sequences(train_labels))
    tuning_label_seq = np.array(label_tokenizer.texts_to_sequences(tuning_labels))

    model = tf.keras.Sequential([tf.keras.layers.Embedding(vocab_size, embedding_dim),
                                 tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(embedding_dim)),
                                 tf.keras.layers.Dense(embedding_dim, activation='relu'),
                                 tf.keras.layers.Dense(6, activation='softmax')])

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    num_epochs = 20

    model.fit(train_padded, training_label_seq, epochs=num_epochs, validation_data=(tuning_padded, tuning_label_seq), verbose=2)

    predictions = []

    test_sequences = tokenizer.texts_to_sequences(test_articles)
    test_padded = pad_sequences(test_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)
    pred = model.predict(test_padded)
    i = 0
    for line in test_articles:
        index = np.argmax(pred[i])
        predictions.append(output[index])
        i += 1

    return predictions

def create_output(predictions, test_input):

    output_name = input("Enter the name of the desired text categorized predictions file: ")

    output_file = open(output_name, 'w')

    test_file = open(test_input, 'r')

    test_file_lines = test_file.read().splitlines()

    i = 0
    for line in test_file_lines:
        line.strip('\n')

        cat = predictions[i]

        output_line = line + ' ' + cat.capitalize() + '\n'

        output_file.write(output_line)

        i += 1

    output_file.close()

    return

train_input = input("Enter the name of the labeled list of training documents: ")
test_input = input("Enter the name of the list of the testing documents to be categorized: ")

articles = []
labels = []
test_articles = []
predictions = []

articles, labels, test_articles = create_lists(train_input, test_input)
predictions = train_and_cat(articles, labels, test_articles, vocab_size, embedding_dim, max_length, trunc_type, padding_type, oov_tok, training_portion)
create_output(predictions, test_input)

###############################################################################
# Using Keras and Tensorflow neural network model
###############################################################################

import numpy as np
import tensorflow as tf
import keras
from keras.models import Sequential, Model
from keras.layers.core import Dense, Activation, Flatten, Dropout
from keras.layers.embeddings import Embedding
from keras.layers import Merge

## Dataset Constants
N_USERS = 458293;  # total number of users
N_MOVIES = 17770;  # total number of movies
N_DAYS = 2243;     # date number is between 1 and 2243 (in days)

BASE_SIZE = 94362233;
VALID_SIZE = 1965045;
HIDDEN_SIZE = 1964391;
PROBE_SIZE = 1374739;
QUAL_SIZE = 2749898;
ALL_SIZE = 102416306;

def load_data(path):
    '''
    Loads dataset from the given path.

    Returns dataset.
    '''
    print('Loading ' + path + ' data...')
    data = np.loadtxt(path).astype(int)
    data = np.delete(data, 2, axis=1)
    data[:, 0] = data[:, 0] - 1
    data[:, 1] = data[:, 1] - 1
    print('Done loading ' + path + ' data...')
    return data

## Load data
train_data_1 = load_data('../data/um/base.dta')
train_data_2 = load_data('../data/um/hidden.dta')
train_data_3 = load_data('../data/um/valid.dta')
train_data = np.concatenate((train_data_1, train_data_2, train_data_3), axis=0)
# train_data = load_data('../data/um/valid.dta')
test_data = load_data('../data/um/probe.dta')
qual_data = load_data('../data/um/qual.dta')
# X_train = train_data[:, 0:2]
# y_train = train_data[:, 2]
# X_test = test_data[:, 0:2]
# y_test = test_data[:, 2]

# Dataset Sizes
train_size = len(train_data)
test_size = len(test_data)

# ## Transform the labels into a one hot vector
# y_train = keras.utils.np_utils.to_categorical(y_train)
# y_test = keras.utils.np_utils.to_categorical(y_test)

## Data Normalization?

## Create your own model here given the constraints in the problem
user_model = Sequential()
user_model.add(Embedding(N_USERS, 60, input_length=1))

movie_model = Sequential()
movie_model.add(Embedding(N_MOVIES, 60, input_length=1))

model = Sequential()
model.add(Merge([user_model, movie_model], mode='concat'))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(64, activation='relu'))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adadelta', metrics=['accuracy'])

## Printing a summary of the layers and weights in your model
print("Model Summary:")
model.summary()

fit = model.fit([train_data[:, 0].reshape(train_size, 1), train_data[:, 1].reshape(train_size, 1)], train_data[:, 2].reshape(train_size, 1), batch_size=20000, epochs=1,
    verbose=1)
print("Model Fitted.")

## Printing the accuracy of our model, according to the loss function specified in model.compile above
score = model.evaluate([test_data[:, 0].reshape(test_size, 1), test_data[:, 1].reshape(test_size, 1)], test_data[:, 2].reshape(test_size, 1), verbose=1)
print('Test score:', score[0])
print('Test accuracy:', score[1])

## Writing Predictions on Probe set
with open('./out/NN_12_probe.dta', 'w+') as out:
    prediction = model.predict([test_data[:,0].reshape(test_size, 1), test_data[:, 1].reshape(test_size, 1)])
    for p in prediction:
        out.write(str(p)+"\n")

## Writing Predictions on Qual set
with open('./out/NN_12.dta', 'w+') as out:
    prediction = model.predict([qual_data[:,0].reshape(QUAL_SIZE, 1), qual_data[:, 1].reshape(QUAL_SIZE, 1)])
    for p in prediction:
        out.write(str(p)+"\n")

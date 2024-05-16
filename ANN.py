from ComponentCollection import ComponentCollection, Component, Rectangle
from ComponentWidget3 import ComponentWidget
from GetData import getJSONDetails, getNetlistDetails
from PlacementValidator import PlacementValidator
from Legalization import Legalization2
# from MainForANN import mainForANN

import tensorflow as tf
import numpy as np
import random
import os
import sys
from PySide6.QtWidgets import QApplication
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense        
from sklearn.preprocessing import StandardScaler   


if __name__ == '__main__':
    # np.random.seed(42)
    # tf.random.set_seed(42)

    # load csv 
    file_path = "data.csv"
    data = pd.read_csv(file_path)

    # csv has columns labeled from 0 to 71 (total of 72 cols)
    # split the data into input (features) and output (labels)
    X = data.iloc[:, :76].values  # 1st 36 cols as input
    y = data.iloc[:, 76:].values  # last 36 cols as output

    # print(X)
    # print(y)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # neural network model
    model = Sequential([
        Dense(76, input_dim=76, activation='relu'),  # input layer w/76 neurons
        Dense(152, activation='relu'),  # hidden layer w/152 neurons
        Dense(304, activation='relu'),  # hidden layer w/304 neurons
        Dense(228, activation='relu'),  # hidden layer w/152 neurons
        Dense(228, activation='relu'),  # hidden layer w/152 neurons
        Dense(152, activation='relu'),  # hidden layer w/152 neurons
        Dense(152, activation='relu'),  # hidden layer w/152 neurons
        Dense(152, activation='relu'),  # hidden layer w/152 neurons
        Dense(152, activation='relu'),  # hidden layer w/76 neurons
        Dense(76, activation='relu'),  # hidden layer w/76 neurons
        Dense(76, activation='linear')  # output layer w/76 neurons
    ])

    # compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    # train
    model.fit(X_scaled, y, epochs=10, batch_size=5)  # together, they're 100000 iterations

    # save the model
    model.save("ann.h5")
    
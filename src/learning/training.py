from keras.models import Sequential
from keras.layers import Dense, Activation, Conv1D, MaxPooling1D, Flatten
import numpy as np
import os

import src.miscellaneous


def get_model():
    return Sequential([
        Conv1D(32, kernel_size=5, input_shape=(514, 12)),
        MaxPooling1D(),
        Activation('relu'),
        Conv1D(64, kernel_size=5),
        MaxPooling1D(),
        Activation('relu'),
        Conv1D(128, kernel_size=5),
        MaxPooling1D(),
        Activation('relu'),
        Flatten(),
        Dense(20),
        Activation('relu'),
        Dense(2),
        Activation('softmax')
    ])


def train_model(trainX, trainY, testX, testY):
    model = get_model()
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(trainX,
              trainY,
              epochs=10,
              batch_size=32,
              validation_data=(testX, testY))

    return model


def create_and_save_networks(root='data/mals/'):
    notes = src.miscellaneous.get_notes()

    for note in notes:
        print("creating net for anomaly", note)
        data = np.load(os.path.join(root, 'mal_' + note + '.mal'))
        model = train_model(data['trainX'], data['trainY'], data['testX'], data['testY'])
        print("saving...")
        model.save(os.path.join('models', 'model_' + note + '.h5'))
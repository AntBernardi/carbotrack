import numpy as np
import pandas as pd

from keras.callbacks import ReduceLROnPlateau
from keras.models import Sequential
from keras.layers import Dense, LSTM, RepeatVector, TimeDistributed, Bidirectional, ConvLSTM2D, Flatten
from keras.callbacks import EarlyStopping
from keras.saving import save_model

def LSTM_model(X_Train, Y_Train, X_Test, Y_Test, epochs=100, batch_size=32):
    """
    Constructs and trains an LSTM model for time series prediction.

    This function builds an LSTM neural network using the Keras library, trains it on the provided training dataset,
    and then makes predictions on both training and test datasets. The predictions are clipped to fall within a
    predefined blood glucose range.

    Parameters:
    X_Train : ndarray
        Training dataset features.
    Y_Train : ndarray
        Training dataset target variable.
    X_Test : ndarray
        Test dataset features.
    Y_Test : ndarray
        Test dataset target variable (not used in the function but typically necessary for evaluating the model).
    epochs : int, optional
        Number of epochs for training the model (default is 100).
    batch_size : int, optional
        Batch size for training the model (default is 32).

    Returns:
    tuple
        A tuple containing predictions for the test and training sets, the trained model, and the training history object.

    Note:
    The function assumes that the number of features in the dataset is 7 and the data is structured for LSTM training.
    It also assumes a specific blood glucose range for clipping the predictions.
    """

    # Reshape input data to be compatible with LSTM layers
    n_timesteps = X_Train.shape[1]
    n_features = 7  # Assumes 7 features in the dataset
    X_Train = X_Train.reshape(X_Train.shape[0], n_timesteps, n_features)

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(200, activation='relu', input_shape=(n_timesteps, n_features)))
    model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    # Callback for early stopping
    earlystop = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=20, min_delta=0.0001, verbose=1)
    callbacks_list = [earlystop]

    # Train the model
    history = model.fit(X_Train, Y_Train, epochs=epochs, batch_size=batch_size, callbacks=callbacks_list, validation_split=0.20, shuffle=False, verbose=0)

    # Make predictions on the training set
    yhat_Train = model.predict(X_Train, verbose=0)

    # Clip predictions to fall within blood glucose range
    min_BG = 40  # Minimum blood glucose level
    max_BG = 400  # Maximum blood glucose level
    yhat_Train = np.where(yhat_Train > max_BG, max_BG, yhat_Train)
    yhat_Train = np.where(yhat_Train < min_BG, min_BG, yhat_Train)

    # Reshape test data and make predictions
    X_Test = X_Test.reshape(X_Test.shape[0], X_Test.shape[1], n_features)
    yhat = model.predict(X_Test, verbose=0)
    yhat = np.where(yhat > max_BG, max_BG, yhat)
    yhat = np.where(yhat < min_BG, min_BG, yhat)

    # Save the model in 2 different extension file
    model.save('models/lstm_model.keras')
    model.save('models/lstm_model.h5')

    return yhat, yhat_Train, model, history

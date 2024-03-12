import datetime
import pandas as pd
import numpy as np

def convert_to_datetime(value):
    """
    Converts a string representing elapsed time since a reference date into a datetime object.

    The function takes a string input in the format "days HH:MM:SS", where 'days' is the number of days since
    a predefined reference date, and 'HH:MM:SS' represents hours, minutes, and seconds elapsed in the last day.
    The reference date is set within the function (default is January 1, 2020).

    Parameters:
    value (str): A string representing time elapsed since the reference date, formatted as "days HH:MM:SS".

    Returns:
    datetime.datetime: A datetime object representing the specific date and time up to seconds resolution.

    Example:
    >>> convert_to_datetime("5 12:30:45")
    datetime.datetime(2020, 1, 6, 12, 30, 45)
    """
    days, time = value.split()
    reference_date = datetime.datetime(2020, 1, 1)  # Modify according to your reference date
    delta = datetime.timedelta(days=int(days))
    time_components = [int(t) for t in time.split(':')]
    return reference_date + delta + datetime.timedelta(hours=time_components[0], minutes=time_components[1], seconds=time_components[2])


def time_interval(datetime_str):
    """
    Computes the 5-minute time interval for a given datetime string.

    Args:
        datetime_str (str): A string representing the datetime in the format '%Y-%m-%d %H:%M:%S'.

    Returns:
        str: A string representing the 5-minute time interval including the date,
             formatted as 'YYYY-MM-DD HH:MM-HH:MM'.

    Example:
        >>> time_interval('2024-03-11 12:32:00')
        '2024-03-11 12:30-12:35'
    """
    # Convert data to datetime type
    datetime_obj = pd.to_datetime(datetime_str, format='%Y-%m-%d %H:%M:%S')

    # Extract date, hour, and minute
    date = datetime_obj.date()
    time = datetime_obj.time()

    # Extract hour and minute
    hour, minute = time.hour, time.minute

    # Find the 5-minute interval
    interval_start = minute - (minute % 5)
    interval_end = interval_start + 5

    # Format the new value
    interval_start_str = f"{hour:02d}:{interval_start:02d}"
    interval_end_str = f"{hour:02d}:{interval_end:02d}" if interval_end < 60 else f"{(hour+1) % 24:02d}:00"

    return f"{date} {interval_start_str}-{interval_end_str}"

def create_sequences(df, sequence_length):
    """
    Transforms a DataFrame into sequences of data suitable for time series forecasting.

    This function creates sequences of a specified length from the DataFrame, dividing each sequence into
    input features (X) and a target value (Y). The target value is the 'Glucose_t+60m' value at the end of each sequence,
    representing the glucose level 60 minutes after the last time step in the sequence.

    Parameters:
    df : DataFrame
        A Pandas DataFrame with time series data and a target column ('Glucose_t+60m').
    sequence_length : int
        The number of time steps to be included in each sequence.

    Returns:
    tuple of numpy.ndarray
        A tuple containing two numpy arrays:
        - X: an array of input sequences, where each sequence is a subarray with the shape (sequence_length, number_of_features).
        - Y: an array of target values, each corresponding to the end of the sequence in X.

    Note:
    The function assumes that the DataFrame is already processed and contains the necessary features along with the
    target column ('Glucose_t+60m'). The target column is not included in the input sequences (X) but is used to create
    the array of target values (Y).
    """
    X = []
    Y = []
    for i in range(len(df) - sequence_length):
        # Select the temporal data sequence
        sequence = df.iloc[i:i+sequence_length]
        # Divide the sequence into input data (X) and target value (Y)
        X.append(sequence.drop(columns=['Glucose_t+60m']).values)
        Y.append(sequence['Glucose_t+60m'].values[-1])

    return np.array(X), np.array(Y)

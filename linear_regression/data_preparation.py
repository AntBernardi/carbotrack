import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time_functions import *

def clean_dataset(basal_file, bolus_file, carbs_file, glucose_file):
    """
    Cleans and merges four datasets related to diabetes management (basal, bolus, carbs, and glucose) into a single DataFrame.

    This function imports data from CSV files, renames and reformats columns for easier merging, merges different datasets based on a common time interval, handles missing data and NaN values, and finally drops unnecessary columns and sorts the final DataFrame.

    Parameters:
    basal_file : str
        The path to the CSV file containing basal insulin data.
    bolus_file : str
        The path to the CSV file containing bolus insulin data.
    carbs_file : str
        The path to the CSV file containing carbohydrate intake data.
    glucose_file : str
        The path to the CSV file containing glucose level data.

    Returns:
    DataFrame
        A cleaned and merged Pandas DataFrame containing all the data from the input files.

    Note:
    This function assumes that each CSV file has a timestamp column named 'Unnamed: 0' and a data column named '0'. It also requires an external `time_interval` function to process the timestamp values.
    """
    # Import datasets
    basal_df = pd.read_csv(basal_file)
    bolus_df = pd.read_csv(bolus_file)
    carbs_df = pd.read_csv(carbs_file)
    glucose_df = pd.read_csv(glucose_file)

    # Prepare new column for merging
    glucose_df['Unnamed: 0'] = pd.to_datetime(glucose_df['Unnamed: 0'])
    glucose_df.rename(columns={"Unnamed: 0": "Timestamp", '0':'Glucose'}, inplace=True)
    glucose_df['TimeInterval'] = glucose_df['Timestamp'].apply(time_interval)

    # Prepare new column for merging
    carbs_df['Unnamed: 0'] = pd.to_datetime(carbs_df['Unnamed: 0'])
    carbs_df.rename(columns={"Unnamed: 0": "Timestamp", '0':'Carbs'}, inplace=True)
    carbs_df['TimeInterval'] = carbs_df['Timestamp'].apply(time_interval)

    # Prepare new column for merging
    basal_df['Unnamed: 0'] = pd.to_datetime(basal_df['Unnamed: 0'])
    basal_df.rename(columns={"Unnamed: 0": "Timestamp", '0':'Basal'}, inplace=True)
    basal_df['TimeInterval'] = basal_df['Timestamp'].apply(time_interval)

    # Prepare new column for mergingt
    bolus_df['Unnamed: 0'] = pd.to_datetime(bolus_df['Unnamed: 0'])
    bolus_df.rename(columns={"Unnamed: 0": "Timestamp", '0':'Bolus'}, inplace=True)
    bolus_df['TimeInterval'] = bolus_df['Timestamp'].apply(time_interval)

    # Merge carbs and bolus insulin values in a temporary df
    temp_df = bolus_df.merge(carbs_df[['Carbs', 'TimeInterval']], on ='TimeInterval')

    # Create a global df to store all data
    clean_df = glucose_df.merge(temp_df[['Bolus', 'Carbs', 'TimeInterval']], how='outer', on='TimeInterval')

    # Merge the last dataframe
    clean_df = clean_df.merge(basal_df[['Basal', 'TimeInterval']], on ='TimeInterval', how='outer')

    # Set average values for Glucose and previous timestamps for Timestamp
    clean_df.Timestamp[0] = '2021-12-07 01:07:00'
    clean_df.Timestamp[1] = '2021-12-07 01:12:00'
    clean_df.Glucose[0] =100
    clean_df.Glucose[1] =100

    # Replace NaN by the average of the previous and next values
    clean_df['Timestamp'] = clean_df['Timestamp'].fillna(clean_df['Timestamp'].interpolate())
    clean_df['Glucose'] = clean_df['Glucose'].fillna(clean_df['Glucose'].interpolate())

    # Replace NaN values by 0.0
    clean_df.replace(to_replace=np.nan, value=0.0, inplace=True)

    # Drop useless column
    clean_df = clean_df.drop(columns='TimeInterval').sort_values(by='Timestamp')

    return clean_df


def feature_engineering(clean_df):
    """
    Performs feature engineering on a cleaned DataFrame of diabetes data.

    This function creates new columns to capture the time elapsed since the last recorded carbohydrate intake,
    bolus insulin dose, and basal insulin dose. It also prepares a target column for future glucose level predictions
    and drops the Timestamp column.

    Parameters:
    clean_df : DataFrame
        A Pandas DataFrame containing cleaned diabetes management data. It should have columns for Carbs,
        Bolus, Basal, and Glucose values.

    Returns:
    DataFrame
        The modified DataFrame with additional engineered features.

    Note:
    The function assumes the DataFrame index is representative of time in a linear fashion, with each step
    corresponding to a fixed interval (e.g., 5 minutes). It also assumes that the 'Glucose' column represents
    the glucose level, and the function creates a target column for glucose levels 60 minutes ahead.
    """
    # Initialisez une nouvelle colonne 'TimeSinceCarbs'
    clean_df['TimeSinceCarbs'] = 0

    # Parcourez le DataFrame pour calculer le temps écoulé depuis la dernière ingestion de glucides
    last_carbs_index = None
    for index, row in clean_df.iterrows():
        if row['Carbs'] != 0:
            last_carbs_index = index
        if last_carbs_index is not None:
            clean_df.at[index, 'TimeSinceCarbs'] = (index - last_carbs_index) * 5

    # Initialisez une nouvelle colonne 'TimeSinceBolus'
    clean_df['TimeSinceBolus'] = 0

    # Parcourez le DataFrame pour calculer le temps écoulé depuis la dernière ingestion de glucides
    last_bolus_index = 0
    for index, row in clean_df.iterrows():
        if row['Bolus'] != 0:
            last_bolus_index = index
        if last_bolus_index is not None:
            clean_df.at[index, 'TimeSinceBolus'] = (index - last_bolus_index) * 5


    # Initialisez une nouvelle colonne 'TimeSinceBasal'
    clean_df['TimeSinceBasal'] = 0

    # Parcourez le DataFrame pour calculer le temps écoulé depuis la dernière ingestion de glucides
    last_basal_index = 0
    for index, row in clean_df.iterrows():
        if row['Basal'] != 0:
            last_basal_index = index
        if last_basal_index is not None:
            clean_df.at[index, 'TimeSinceBasal'] = (index - last_basal_index) * 5

    # Nouvelle colonne target à 1h
    clean_df['Glucose_t+60m'] = clean_df['Glucose'].shift(-12)

    # Drop Timestamp column
    clean_df = clean_df.drop(columns='Timestamp')

    return clean_df

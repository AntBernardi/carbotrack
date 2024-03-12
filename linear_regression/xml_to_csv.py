import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import os

# Function to convert XML data to CSV format
def XMLtoCSV(patient_ids, data_type='glucose_value'):
    """
    Converts XML data to CSV format.

    Args:
        patient_ids (list): List of patient IDs.
        data_type (str, optional): Type of data. Defaults to 'glucose_value'.

    Returns:
        None
    """
    # List of subsets (training and testing)
    subset_list = ['training', 'testing']

    # Iterate over each patient ID
    for patient_id in patient_ids:
        # Iterate over each subset
        for subset in subset_list:
            # Construct the filename based on patient ID and subset
            file_name = os.path.join('data', f"{patient_id}-ws-{subset}.xml")

            try:
                # Attempt to parse the XML file
                tree = ET.parse(file_name)
                root = tree.getroot()
                Glucose = root[0]
                GlucoseChildren = list(Glucose)
                Basal = root[2]
                BasalChildren = list(Basal)
                Bolus = root[4]
                BolusChildren = list(Bolus)

                TS = []
                BGV = []
                TS_BASAL = []
                BASAL = []
                TS_BOLUS = []
                BOLUS = []
                CARBS = []

                # Extract timestamp and glucose value from each XML element
                for child in GlucoseChildren:
                    ts = child.attrib['ts']
                    TS.append(ts)
                    value = child.attrib['value']
                    BGV.append(value)
                # Extract timestamp and basal value from each XML element
                for child in BasalChildren:
                    ts_basal = child.attrib['ts']
                    TS_BASAL.append(ts_basal)
                    basal_value = child.attrib['value']
                    BASAL.append(basal_value)
                # Extract timestamp, carbs and insuline dose values from each XML element
                for child in BolusChildren:
                    ts_bolus = child.attrib['ts_begin']
                    TS_BOLUS.append(ts_bolus)
                    dose_bolus = child.attrib['dose']
                    BOLUS.append(dose_bolus)
                    carbs_intake = child.attrib['bwz_carb_input']
                    CARBS.append(carbs_intake)

                # Format timestamps and create a pandas Series
                TS_new = [datetime.strptime(ts, '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') for ts in TS]
                data = pd.Series(BGV, index=TS_new)

                # Create serie for basal
                TS_BASAL_NEW = [datetime.strptime(ts, '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') for ts in TS_BASAL]
                basal_data = pd.Series(BASAL, index=TS_BASAL_NEW)

                # Create serie bolus dose
                TS_BOLUS_NEW = [datetime.strptime(ts, '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') for ts in TS_BOLUS]
                bolus_data = pd.Series(BOLUS, index=TS_BOLUS_NEW)

                # Create serie bolus dose
                TS_CARBS_NEW = [datetime.strptime(ts, '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') for ts in TS_BOLUS]
                carbs_data = pd.Series(CARBS, index=TS_CARBS_NEW)

                # Save the data as a CSV file
                data.to_csv(f"{data_type}_{patient_id}_{subset}.csv")
                basal_data.to_csv(f"{data_type}_{patient_id}_{subset}_basal.csv")
                bolus_data.to_csv(f"{data_type}_{patient_id}_{subset}_bolus.csv")
                carbs_data.to_csv(f"{data_type}_{patient_id}_{subset}_carbs.csv")

            except FileNotFoundError:
                # Handle the case when the XML file is not found
                print(f"File {file_name} does not exist.")

# List of patient IDs
patient_ids = ['559', '563', '570', '575', '588', '591']

# Call the function to convert XML data to CSV for each patient
XMLtoCSV(patient_ids)

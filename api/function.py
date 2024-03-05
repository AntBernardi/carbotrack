import json
import numpy as np
import pandas as pd
from transformers import pipeline
from google.cloud import bigquery
from carbotrack_code.params import *
from PIL import Image
import io

# Get the path of the JSON key file from the environment variable
key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Use the key file to authenticate
client = bigquery.Client.from_service_account_json(key_path)

def get_food(image: Image.Image):
    model = pipeline("image-classification", model="nateraw/food", framework="pt")
    predict = model.predict(image)
    food_result = predict[0]['label'].upper()
    return food_result

def get_carbs (food_result):

    query = f"""
        SELECT Data_Carbohydrate, Data_Household_Weights_1st_Household_Weight,Data_Household_Weights_1st_Household_Weight_Description
        FROM `{GCP_PROJECT}.nutrition_table.main`
        WHERE Category = '{food_result}'
    """
    client = bigquery.Client(project=GCP_PROJECT)
    query_job = client.query(query)
    query_result = query_job.result()
    print(query_result)
    df = query_result.to_dataframe()
    carbs_result = df['Data_Carbohydrate'].mean()
    return carbs_result

def get_insuline(carbs_result):
    if pd.isnull(carbs_result):
        return None
    else:
        return round(carbs_result / 15)

def safe_json(data):
    def handle_value(x):
        if isinstance(x, float):
            if np.isfinite(x):
                return x
            else:
                return str('Data not found, sorry our model is still learning ;)')  # or replace with a default value
        return x
    return json.dumps(data, default=handle_value)

def get_full_result(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    food_result = get_food(image)
    carbs_result = get_carbs(food_result)
    insuline_result = get_insuline(carbs_result)
    return food_result, carbs_result, insuline_result

def create_response(image_bytes):
    food_result, carbs_result, insuline_result = get_full_result(image_bytes)
    data = {
        'food_result': food_result,
        'carbs_result': carbs_result,
        'insuline_result': insuline_result
    }
    return safe_json(data)

if __name__ == '__main__':
    pass
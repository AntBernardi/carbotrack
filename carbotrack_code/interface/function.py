import pandas as pd
from transformers import pipeline
from google.cloud import bigquery
from params import GCP_PROJECT
from PIL import Image
import io
import os
import json
import numpy as np

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

    df = pd.read_csv('raw_data/food1.csv')
    mask = df['Category'] == food_result
    df_result = df[mask]
    carbs_result = df_result['Data.Carbohydrate'].mean()
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

def get_insuline (carbs_result):
    insuline_result = round(carbs_result/15)
    return insuline_result

# def get_full_result (image):
#     food_result = get_food(image)
#     carbs_result = get_carbs(food_result)
#     insuline_result = get_insuline(carbs_result)
#     return food_result,carbs_result,insuline_result


if __name__ == '__main__':
    pass
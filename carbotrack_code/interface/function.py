import pandas as pd
from transformers import pipeline
from google.cloud import bigquery
from carbotrack_code.params import GCP_PROJECT

from PIL import Image
import io
import os
import json
import numpy as np
import requests


def get_food (model,image):

    predict = model.predict(image)
    food_result = predict[0]['label'].upper()
    return food_result



def get_carbs (food_result, image_path):

    #request API volume
    url = 'https://food-weight-estimation-4xnsxy3ska-od.a.run.app/predict'
    params = {'food_type': food_result, 'plate_diameter': '0'}

    files = {'image': ('image24.jpeg', open(image_path, 'rb'), 'image/jpeg')}
    headers = {
        'accept': 'application/json',
    }
    response = requests.post(url, params=params, files=files, headers=headers)
    result_volume = round(response.json()['weight'],2)

    # request from cyrill Api spoonacular
    url_carbo = 'https://carbotrackv1-7xel7l3dia-ew.a.run.app/predict'

    params_carbo = {'food_type': food_result, 'plate_diameter': '0'}

    files = {'image': ('image24.jpeg', open(image_path, 'rb'), 'image/jpeg')}
    headers = {
        'accept': 'application/json',
    }
    response = requests.post(url_carbo, params=params_carbo, files=files, headers=headers)
    result_carbo = round(response.json()['carbs_result'],2)


    carbs_result = round((result_volume * result_carbo)/150,2)

    return carbs_result

def get_insuline(carbs_result):
    if pd.isnull(carbs_result):
        return None
    else:
        return round(carbs_result / 9)


def safe_json(data):
    def handle_value(x):
        if isinstance(x, float):
            if np.isfinite(x):
                return x
            else:
                return str('Data not found, sorry our model is still learning ;)')  # or replace with a default value
        return x
    return json.dumps(data, default=handle_value)

def get_full_result(model,image_bytes):
    food_result = get_food(model,image_bytes)
    carbs_result = get_carbs(food_result,image_bytes)
    insuline_result = get_insuline(carbs_result)
    return food_result, carbs_result, insuline_result

def create_response(model,image_bytes):
    food_result, carbs_result, insuline_result = get_full_result(model,image_bytes)
    data = {
        'food_result': food_result,
        'carbs_result': carbs_result,
        'insuline_result': insuline_result
    }
    return safe_json(data)


if __name__ == '__main__':
    pass

import sys
import os

# Get the directory of the current file
current_dir = os.path.dirname(os.path.realpath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)
from fastapi import FastAPI
from carbotrack_code.interface.function import get_full_result


app = FastAPI()

# Define a root `/` endpoint
@app.get('/')
def index():
    return {'Hello': 'You'}

@app.get('/predict')
def predict(image):
    food_result,carbs_result,insuline_result = get_full_result(image)
    return {'You are eating': food_result,
            'Carbs quantity': carbs_result,
            'Insuline doses recommended': insuline_result}

@app.get('/dummy_test')
def dummy(int: int):
    if int == 1:
        return {'One'}
    else:
        return {'Please input 1 as parameter'}    
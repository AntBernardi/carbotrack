import sys

sys.path.insert(0, '/home/daliryc/code/AntBernardi/carbotrack')

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
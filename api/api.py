import sys
import os
import uuid


# Get the directory of the current file
current_dir = os.path.dirname(os.path.realpath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)


from fastapi import FastAPI, UploadFile
from fastapi.param_functions import File
from fastapi.responses import JSONResponse
from carbotrack_code.interface.function import get_full_result, create_response, safe_json
from carbotrack_code.interface.function import get_food, get_carbs, get_insuline
from fastapi.staticfiles import StaticFiles
from PIL import Image
import io
import json
from fastapi import FastAPI
from carbotrack_code.interface.function import get_full_result


app = FastAPI()

# Define a root `/` endpoint
@app.get('/')
def index():
    return {'Hello': 'You'}

# Serve files from the /images directory at the /images URL
app.mount("/images", StaticFiles(directory="images"), name="images")

@app.post('/first_step')
async def first_step(image: UploadFile = File(...)):
    try:
        if not image.content_type.startswith("image/"):
            return JSONResponse(status_code=400, content={"error": "Invalid file type"})
        
        filename = f"{uuid.uuid4()}.jpg"
        image_path = f'images/{filename}'

        with open(image_path, 'wb') as buffer:
            contents = await image.read()
            buffer.write(contents)

        food_result = get_food(image_path)

        return {'You are eating': food_result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"An error occurred: {e}"})

@app.post('/get_carbs')
async def get_carbs_endpoint(image: UploadFile = File(...)):
    try:
        if not image.content_type.startswith("image/"):
            return JSONResponse(status_code=400, content={"error": "Invalid file type"})
        
        filename = f"{uuid.uuid4()}.jpg"
        image_path = f'images/{filename}'
        with open(image_path, 'wb') as buffer:
            contents = await image.read()
            buffer.write(contents)
        food_result = get_food(image_path)
        carbs_result = get_carbs(food_result)
        return {
            'You are eating': food_result,
            'Carbohydrate content': carbs_result
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"An error occurred: {e}"})

@app.get('/get_carbs/{food_result}')
async def get_carbs_endpoint(food_result: str):
    carbs_result = get_carbs(food_result)
    return {
        'You are eating': food_result,
        'Carbohydrate content': carbs_result
    }

# @app.post('/predict')
# async def predict(image: UploadFile = File(...)):
#     try:
#         contents = await image.read()
#         food_result, carbs_result, insuline_result = get_full_result(contents)
#         return {
#             'You are eating': food_result,
#             'Carbs quantity': carbs_result,
#             'Insuline doses recommended': insuline_result
#         }
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": f"An error occurred: {e}"})

# @app.post('/predict')
# async def predict(image: UploadFile = File(...)):
#     try:
#         contents = await image.read()
#         response = create_response(contents)
#         return JSONResponse(status_code=200, content=json.loads(response))
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": f"An error occurred: {e}"})

@app.post('/predict')
async def predict(image: UploadFile = File(...)):
    try:
        contents = await image.read()
        response = create_response(contents)
        response_json = json.loads(response)

        # Truncate or limit the size of the response
        if len(str(response_json)) > 1000:  # Change 1000 to the maximum size you want
            response_json = str(response_json)[:1000]  # Truncate the response

        return JSONResponse(status_code=200, content=response_json)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"An error occurred: {e}"})

# @app.get('/predict')
# def predict(image):
#     food_result,carbs_result,insuline_result = get_full_result(image)
#     return {'You are eating': food_result,
#             'Carbs quantity': carbs_result,
#             'Insuline doses recommended': insuline_result}


@app.get('/dummy_test')
def dummy(int: int):
    if int == 1:
        return {'One'}
    else:
        return {'Please input 1 as parameter'}    
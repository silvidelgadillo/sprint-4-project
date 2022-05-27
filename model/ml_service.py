# aca el modelo agarra la informacion de redis para procesarla

import time
import redis
import settings
import json

from tensorflow.keras.applications import resnet50
from tensorflow.keras.preprocessing import image

import matplotlib.pyplot as plt
import numpy as np


# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(       
    host = settings.REDIS_IP, 
    port = settings.REDIS_PORT, 
    db   = settings.REDIS_DB_ID,
)

# Connect to Redis
assert db.ping, "I couldnt connect"


# TODO
# Load your ML model and assign to variable `model`

model = resnet50.ResNet50(include_top=True, weights="imagenet")


def predict(image_name):
    """
    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.

    Parameters
    ----------
    image_name : str
        Image filename.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    # TODO
    # le cambiamos el tamaño porque el modelo esta entrenado con imagenes cuadradas de 224x224:
    img = image.load_img(image_name, target_size=(224, 224))
    # creo una dimension nueva:
    x = np.expand_dims(x, axis=0)
    # preproceso:
    x = resnet50.preprocess_input(x)

    # Get predictions
    preds = model.predict(x)

    # esto da como resultado un pillow--> lo convierto en array:
    x = image.img_to_array(img)

    # el modelo esta entrenado para devolverte la probabilidad de 1000 clases. por eso devuelve una lista de 1x1000. 
    # elijo la mas probable:
    

    return resnet50.decode_predictions(preds, top=1)


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    while True:
        #   1. Take a new job from Redis

        # job_data es un un dict con 'id" and 'image_name'
        # buscar la info
        # brpop llama al primero de la fila, ojo trae dos variables
        _, data_json       =  db.brpop(settings.REDIS_QUEUE) 
        
        # proceso inverso de string a diccionario:
        data_dictionary    = json.loads(data_json) # aca tenemos job_id y el nombre

        # we call to the predict function and Store model prediction in a dict:
        #      {
        #         "prediction": str,
        #         "score": float,
        #      }
        
        #   2. Run your ML model on the given data
        class_name, score = predict(data_dictionary['image_name'])

        # esto lo tenemos que mandar a traves de middleware a redis:
        prediction_dictionary = {"prediction": class_name , "score": score }
        
        #   4. Store the results on Redis using the original job ID as the key
        #      so the API can match the results it gets to the original job
        #      sent
        db.set(data_dictionary['id'], json.dumps(prediction_dictionary)) 

        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()

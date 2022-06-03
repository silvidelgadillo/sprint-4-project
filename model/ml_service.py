import time
import settings
import redis
import json
import os
from tensorflow.keras.applications import resnet50
from tensorflow.keras.preprocessing import image
import numpy as np

# REDIS
# Redis es un motor de base de datos en memoria, basado en el almacenamiento
# en tablas de hashes pero que opcionalmente puede ser usada
# como una base de datos durable o persistente

# TABLA HASHES
# tabla fragmentada es una estructura de datos que 
# asocia llaves o claves con valores. permite el acceso a los 
# elementos almacenados a partir de una clave generada


# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host = settings.REDIS_IP,
    port = settings.REDIS_PORT,
    db = settings.REDIS_DB_ID,
    )

# El uso de assert en Python nos permite realizar comprobaciones. 
# Si la expresión contenida dentro del mismo es
# False, se lanzará una excepción, concretamente AssertionError (o la indicada "")
# assert db.ping, "unable to connect"
 


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
    
    image_name = image.load_img(os.path.join(settings.UPLOAD_FOLDER, image_name), target_size=(224, 224))
    image_array = image.img_to_array(image_name)
    image_expand = np.expand_dims(image_array, axis=0)
    image_preproce = resnet50.preprocess_input(image_expand)
    preds_resnet50 = model.predict(image_preproce)
    preds_decode = resnet50.decode_predictions(preds_resnet50, top=1)
    class_name = preds_decode[0][0][1]
    pred_probability = round(float(preds_decode[0][0][2]), 4)
    
    return tuple([class_name, pred_probability])
    

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
        # Inside this loop you should add the code to:
        #   1. Take a new job from Redis
        #   2. Run your ML model on the given data
        #   3. Store model prediction in a dict with the following shape:
        #      {
        #         "prediction": str,
        #         "score": float,
        #      }
        #   4. Store the results on Redis using the original job ID as the key
        #      so the API can match the results it gets to the original job
        #      sent
        # Hint: You should be able to successfully implement the communication
        #       code with Redis making use of functions `brpop()` and `set()`.
        
        # traigo lo primero que esta en queue
        _, data_json = db.brpop(settings.REDIS_QUEUE)
        data_dict = json.loads(data_json) # convert JSON str to a dict of Python
        prediction, score = predict(data_dict["image_name"])
        predict_dict = {"prediction":prediction , "score":score}
        db.set(data_dict["id"], json.dumps(predict_dict)) # serializa los objetos python a str
        
        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)
        

if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()


# REDIS COMMANDS
# BRPOP:  extrae un elemento de queue de la primera lista que no está vacía,
# y las claves dadas se verifican en el orden en que se dan.

# SET: Set key to hold the string value. 
# If key already holds a value, it is overwritten, regardless of its type.

# RPUSH: Insert all the specified values at the tail of the list stored at key. 
# If key does not exist, it is created as empty list before performing the push operation. 
# When key holds a value that is not a list, an error is returned.
# It is possible to push multiple elements using a single command call
# just specifying multiple arguments at the end of the command. 
# Elements are inserted one after the other to the tail of the list,
# from the leftmost element to the rightmost element. 
# So for instance the command RPUSH mylist a b c will result into a list 
# containing a as first element, b as second element and c as third element
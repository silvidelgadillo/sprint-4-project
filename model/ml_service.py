import time
import redis
import settings
from tensorflow.keras.applications import resnet50
from tensorflow.keras.preprocessing import image
import os
import json
import numpy as np


# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host= settings.REDIS_IP, 
    port= settings.REDIS_PORT, 
    db= settings.REDIS_DB_ID
)

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
    path = os.path.join(settings.UPLOAD_FOLDER, image_name)
    img = image.load_img(path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    preproc_img = resnet50.preprocess_input(img)
    preds = model.predict(preproc_img)
    prediction_array = resnet50.decode_predictions(preds, top=1)[0][0]
    prediction = prediction_array[1].capitalize()
    score = round(float(prediction_array[2]), 4)

    return prediction, score


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
        # TODO
        _,data = db.brpop(settings.REDIS_QUEUE)
        data_dic = json.loads(data)
        image_create = data_dic["image_name"]
        predict_plus, plus_score = predict(image_create)
        response_dic = {
                "prediction": predict_plus,
                 "score": plus_score,
              }
        db.set(data_dic["id"], json.dumps(response_dic))

        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()

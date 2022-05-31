import time
import redis
import settings
import json
import numpy as np

from tensorflow import keras
from tensorflow.keras.applications.resnet50 import ResNet50, decode_predictions, preprocess_input 
from keras.preprocessing.image import image

# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis( 
        host=settings.REDIS_IP,
        port=settings.REDIS_PORT, 
        db=settings.REDIS_DB_ID
        )

# TODO
# Load your ML model and assign to variable `model`

model = ResNet50(include_top = True, weights='imagenet')


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
    image1 = image.load_img(settings.UPLOAD_FOLDER+image_name, target_size =(224,224)) #load the image
    image_array = image.img_to_array(image1)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = preprocess_input(image_array)

    pred = model.predict(image_array)

    pred_label = decode_predictions(pred, top = 1)[0][0]
    img_class = str(pred_label[1])
    score = round(float(pred_label[2]), 4)
    return tuple([img_class, score])


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
        #job_to_process = nan
        job_to_process =json.loads(db.brpop(settings.REDIS_QUEUE)[1])
        if(job_to_process):
            img_class, precit_confidence = predict(job_to_process['image_name'])
            result_dict = {
                'prediction' : img_class,
                'score' : precit_confidence
                }
            db.set(job_to_process['id'], json.dumps(result_dict))
        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()

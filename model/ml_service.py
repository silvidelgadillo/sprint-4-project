import time
import numpy as np
from tensorflow.keras.applications import resnet50
from tensorflow.keras.preprocessing import image
import settings
import json
import redis
import os


# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID,
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
    img_path = os.path.join(settings.UPLOAD_FOLDER, image_name)
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = resnet50.preprocess_input(x)
    # Get predictions
    preds = model.predict(x)
    pred_to_deliver = resnet50.decode_predictions(preds, top=1)
    predict_class = pred_to_deliver[0][0][1]
    score = round(float(pred_to_deliver[0][0][2]), 4)

    return predict_class, score


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
        time.sleep(settings.SERVER_SLEEP)
        # Inside this loop you should add the code to:
        #    1. Take a new job from Redis
        _, msg = db.brpop(settings.REDIS_QUEUE)
        if msg:
            msg_dict = json.loads(msg)
            #    2. Run your ML model on the given data
            predict_class, score = predict(msg_dict["image_name"])
            #    3. Store model prediction in a dict with the following shape:
            #       {
            #         "prediction": str,
            #         "score": float,
            #      }
            prediction_dict = {
                "prediction": predict_class,
                "score": score,
            }
            #    4. Store the results on Redis using the original job ID as the key
            #      so the API can match the results it gets to the original job
            #      sent
            # Hint: You should be able to successfully implement the communication
            #       code with Redis making use of functions `brpop()` and `set()`.
            # TODO
            db.set(msg_dict["id"], json.dumps(prediction_dict))


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()

from tensorflow.keras.applications import resnet50
from tensorflow.keras.preprocessing import image

import numpy as np
import json
import time
import redis
import settings


db = redis.Redis(
    host = settings.REDIS_IP,
    port = settings.REDIS_PORT, 
    db = settings.REDIS_DB_ID
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
    # Loading image and preprocess
    try:
        img = image.load_img(f"{settings.UPLOAD_FOLDER}{image_name}", target_size=(224, 224))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = resnet50.preprocess_input(img)
    except:
        print("Error while loading image")
        return None

    # Get predictions
    preds = model.predict(img)
    _, class_name, pred_probability = resnet50.decode_predictions(preds, top=1)[0][0]

    return class_name, float(pred_probability)


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.
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

        _, job_data_str = db.brpop(settings.REDIS_QUEUE)
        job_data = json.loads(job_data_str)

        pred_class, pred_score = predict(job_data["image_name"])

        pred_data = {
            "prediction": pred_class,
            "score": pred_score
        }

        pred_data_str = json.dumps(pred_data)

        db.set(job_data["id"], pred_data_str)

        
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...") 
    classify_process()

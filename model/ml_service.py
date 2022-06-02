from tensorflow.keras.applications import resnet50
from tensorflow.keras.preprocessing import image
from tensorflow import config
import os
import numpy as np
import json
import time
import redis
import settings


db = redis.Redis(
    host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID
)

# Prevent tensorflow to allocate the entire GPU
physical_devices = config.list_physical_devices("GPU")
try:
    config.experimental.set_memory_growth(physical_devices[0], True)
except:
    pass

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
    img_path = os.path.join(settings.UPLOAD_FOLDER, image_name)
    img = image.load_img(img_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = resnet50.preprocess_input(img)

    # Get predictions
    preds = model.predict(img)
    _, class_name, pred_probability = resnet50.decode_predictions(preds, top=1)[0][0]
    pred_probability = round(float(pred_probability), 4)

    return class_name, pred_probability


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.
    """
    while True:
        _, job_data_str = db.brpop(settings.REDIS_QUEUE)
        job_data = json.loads(job_data_str)

        pred = predict(job_data["image_name"])
        pred_class, pred_score = pred
        pred_data = {"prediction": pred_class, "score": round(pred_score, 4)}
        pred_data_str = json.dumps(pred_data)

        db.set(job_data["id"], pred_data_str)
        time.sleep(settings.SERVER_SLEEP)


def first_prediction():
    """Make a fake first prediction when running the containers
    to avoid first time loading time of the model.
    """

    img_path = os.path.join("tests/dog.jpeg")
    img = image.load_img(img_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    model.predict(img)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    first_prediction()
    classify_process()

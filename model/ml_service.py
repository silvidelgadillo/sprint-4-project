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


def predict(image_names):
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
    images = []

    # Loading images and preprocess
    for image_name in image_names:
        img_path = os.path.join(settings.UPLOAD_FOLDER, image_name)
        img = image.load_img(img_path, target_size=(224, 224))
        img = image.img_to_array(img)
        images.append(img)

    images = np.array(images)
    images = resnet50.preprocess_input(images)

    # Get predictions
    preds = model.predict(images)
    preds = resnet50.decode_predictions(preds, top=1)

    class_names = []
    pred_probabilities = []

    for pred in preds:
        _, class_name, pred_probability = pred[0]
        pred_probability = round(float(pred_probability), 4)
        class_names.append(class_name)
        pred_probabilities.append(pred_probability)

    return class_names, pred_probabilities


def classify_process(batch_size=1):
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.
    """
    while True:
        jobs_data = []
        received = 0

        while received <= batch_size:
            job = db.brpop(settings.REDIS_QUEUE, timeout=0.3)
            
            if job == None and received == 0:
                continue
            elif job == None and received > 0:
                break

            _, job_data_str = job
            job_data = json.loads(job_data_str)
            jobs_data.append(job_data)
            received += 1

        image_names = []

        for job_element in jobs_data:
            image_names.append(job_element["image_name"])
        
        preds = predict(image_names)
        pred_classes, pred_scores = preds
        preds_data = {"classes": pred_classes, "scores": pred_scores}
        preds_data_str = json.dumps(preds_data)

        for job_element, pred_element in zip(jobs_data, preds_data_str):
            db.set(job_element["id"], pred_element)
        
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

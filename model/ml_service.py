import json
from os import path
import time
from tensorflow.keras.applications import resnet50
from tensorflow.keras.preprocessing import image
import numpy as np
import redis
import settings

# Connect to Redis and assign to variable `db``
db = redis.Redis(
                host =settings.REDIS_IP,
                port =settings.REDIS_PORT,
                db = settings.REDIS_DB_ID,
                )

# Load your ML model and assign to variable `model`
model = resnet50.ResNet50(
                          include_top=True, 
                          weights="imagenet"
                         )


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
    img = image.load_img(path.join(settings.UPLOAD_FOLDER, image_name), target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = resnet50.preprocess_input(img_array)
    
    pred = model.predict(img_array)
    prediction = resnet50.decode_predictions(pred, top=1)
    
    class_name = prediction[0][0][1]
    pred_probability = round(float(prediction[0][0][2]),4)
    
    return class_name, pred_probability


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
        _, new_job = db.brpop(settings.REDIS_QUEUE)
        new_job = json.loads(new_job)

        #   2. Run your ML model on the given data
        prediction, predict_score = predict(new_job["image_name"])

        #   3. Store model prediction in a dict
        pred = {
                "prediction": prediction, 
                "score": predict_score
               }

        #   4. Store the results on Redis using the original job ID as the key
        response = json.dumps(pred)
        db.set(new_job["id"], response)

        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()

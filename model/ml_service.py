import time
import settings
import json
import redis
import os
from tensorflow.keras.applications import resnet50
from tensorflow.keras.preprocessing import image
import numpy as np

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
    locat_img = os.path.join(settings.UPLOAD_FOLDER, image_name)
    prev_img = image.load_img(locat_img, target_size=(224, 224))
    img_to_pred = image.img_to_array(prev_img)
    img_to_pred = np.expand_dims(img_to_pred, axis=0)
    img_to_pred = resnet50.preprocess_input(img_to_pred)

    pred_result = model.predict(img_to_pred)
    final_result = resnet50.decode_predictions(pred_result, top=1)

    return final_result[0][0][1], round(float(final_result[0][0][2]), 4)


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
        # Step 1
        queue_name, job_data_name = db.brpop(settings.REDIS_QUEUE)
        job_data_name = json.loads(job_data_name)
        image_name = job_data_name['image_name']
        # Step 2
        pred_name, pred_score = predict(image_name)
        # Step 3
        output_job_data = {
            'prediction': pred_name,
            'score': pred_score
            }
        # Step 4
        db.set(job_data_name['id'], json.dumps(output_job_data))

        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()

import time
import redis
import settings
import json

# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host=settings.REDIS_HOST_NAME, 
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID
)

# Load your ML model and assign to variable `model`
model = None # ResNet50


def predict(img_name):
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
    return tuple(["Eskimo_dog", 0.9346]) # dummy model until finish the rest


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

        _, json_redis_msg = db.brpop(settings.REDIS_QUEUE)
        redis_msg = json.loads(json_redis_msg)

        id         = redis_msg['id']
        image_name = redis_msg['image_name']

        #   2. Run your ML model on the given data
        
        pred_class, pred_score = predict(image_name) 

        #   3. Store model prediction in a dict with the following shape:
        
        output_msg = {
            "prediction": pred_class,
            "score": pred_score,
        }

        #   4. Store the results on Redis using the original job ID as the key
        #      so the API can match the results it gets to the original job
        #      sent
        # Hint: You should be able to successfully implement the communication
        #       code with Redis making use of functions `brpop()` and `set()`.

        db.set(id, json.dumps(output_msg))

        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()

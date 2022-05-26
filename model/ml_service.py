import time
# import tensorflow as tf
# from tensorflow import keras
# from keras.applications.resnet import ResNet50
import settings
import json
import redis

# model = ResNet50(weights='imagenet')
db = redis.Redis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID
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
    # TODO
    return 'Cat', 0.9999


def classify_process():
    while True:
        time.sleep(settings.SERVER_SLEEP)
        
        queue_name, msg = db.brpop(settings.REDIS_QUEUE)
        msg = json.loads(msg)
        image_name = msg['image_name']

        pred_class, pred_score = predict(image_name)

        output_msg = {
            'prediction': pred_class, 
            'score': pred_score
            }

        db.set(msg['id'], json.dumps(output_msg))


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()

import json
import redis
import settings
import uuid
import time


db = redis.Redis(
    host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID
)


def model_predict(image_name):
    """
    Receives an image name and queues the job into Redis.
    Will loop until getting the answer from our ML service.

    Parameters
    ----------
    image_name : str
        Name for the image uploaded by the user.

    Returns
    -------
    prediction, score : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """

    job_id = str(uuid.uuid4())

    job_data = {
        "id": job_id,
        "image_name": image_name,
    }

    job_data_str = json.dumps(job_data)

    db.rpush(settings.REDIS_QUEUE, job_data_str)

    # Loop until we received the response from our ML model
    while True:
        pred_data_str = db.get(job_data["id"])

        if pred_data_str:
            db.delete(job_data["id"])
            break

        time.sleep(settings.API_SLEEP)

    pred_data = json.loads(pred_data_str)

    pred_class = pred_data["prediction"]
    pred_score = pred_data["score"]

    return pred_class, pred_score

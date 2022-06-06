import time
import settings
import json
import redis
from uuid import uuid4

# Connect to Redis and assign to variable `db``
db = redis.Redis(
                 host =settings.REDIS_IP,
                 port =settings.REDIS_PORT,
                 db = settings.REDIS_DB_ID
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
    # Assign an unique ID for this job and add it to the queue.
    job_id = str(uuid4())

    # Create a dict with the job data we will send through Redis
    job_data = {
                "id":job_id,
                "image_name":image_name
               }

    # Send the job to the model service using Redis
    db.rpush(settings.REDIS_QUEUE,json.dumps(job_data))

    # Loop until we received the response from our ML model
    output=None
    while output==None:
        # Attempt to get model predictions using job_id
        output = db.get(job_data["id"])

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)

    
    output = json.loads(output)
    predict, predict_score = output["prediction"], output["score"]

    # Delete the job from Redis after we get the results!
    db.delete(job_data["id"],settings.REDIS_QUEUE)
    output=None

    return predict, predict_score

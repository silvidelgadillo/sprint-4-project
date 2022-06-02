import time
import uuid
import settings
import json
import redis
   


# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.

db = redis.Redis(
    host = settings.REDIS_IP, 
    port = settings.REDIS_PORT, 
    db   = settings.REDIS_DB_ID
)



def model_predict(image_name):
    """
    Receives an image name and queues the job into Redis.
    Will loop until getting the answer from our ML service.
    """

    job_id = str(uuid.uuid4())
    job_data = {
        "id": job_id,
        "image_name": image_name,
    }

    job_data_str = json.dumps(job_data)
    db.rpush("queue",job_data_str)

    while True:
        if db.get(job_id):
            output = json.loads(db.get(job_id))
            db.delete(job_id)
            break

    time.sleep(settings.API_SLEEP)

    return output["prediction"], output["score"]

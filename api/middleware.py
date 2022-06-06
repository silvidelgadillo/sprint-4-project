import time
import uuid
import redis
import settings
import json

# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host=settings.REDIS_HOST_NAME,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID,
)
# assert db.ping()  # api connection checkpoint


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
    # We need to assing this ID because we must be able to keep track
    # of this particular job across all the services

    job_id = str(uuid.uuid4())

    # Create a dict with the job data we will send through Redis having the
    # following shape:

    job_data = {"id": job_id, "image_name": image_name}

    # Send the job to the model service using Redis
    # Hint: Using Redis `rpush()` function should be enough to accomplish this.

    job_data_str = json.dumps(
        job_data
    )  # transform pair of id-name dict into json because rpush only admits str
    db.rpush(
        settings.REDIS_QUEUE, job_data_str
    )  # rpush(queue_name, message) > we include pair id-name in message

    # Loop until we received the response from our ML model
    while True:
        # Attempt to get model predictions using job_id
        # Hint: Investigate how can we get a value using a key from Redis

        if db.get(job_id):  # check if predict exists

            output = json.loads(db.get(job_id))

            # Don't forget to delete the job from Redis after we get the results!
            # Then exit the loop

            db.delete(job_id)
            break

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)

    return output["prediction"], output["score"]
    # tuple([output['prediction'], output['score']])

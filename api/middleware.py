## here we comunicate views and ml service

import time
import settings
import redis
from utils import get_file_hash
import json
import uuid #para generar id unico
import queue


# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(       
    host = settings.REDIS_IP, 
    port = settings.REDIS_PORT, 
    db   = settings.REDIS_DB_ID
)


# Connect to Redis
# assert db.ping(), "I couldn't connect"


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


    ## redis (comunica con strings) and middleware connect each other or with dictionaries or with strings
    # TODO
    job_id = str(uuid.uuid4())

    # Create a dict with the job data we will send through Redis having the
    # following shape:
    # {
    #    "id": str,
    #    "image_name": str,
    # }
    # TODO  
    job_data = {
        "id": job_id,
        "image_name": image_name,
    }

    # Send the job to the model service using Redis
    # Hint: Using Redis `rpush()` function should be enough to accomplish this.
    # TODO
    ## here we transform to json because redis reads that
    ## db is my redis
    db.rpush(settings.REDIS_QUEUE, json.dumps(job_data))


    # Loop until we received the response from our ML model
    clase = ""
    score = 0  

    while True:
        # Attempt to get model predictions using job_id
        # Hint: Investigate how can we get a value using a key from Redis
        # TODO
        if(db.exists(job_id)):  #if the process exist, do all the following
            output = db.get(job_id)
            output_dictionary = json.loads(output) #take the output and convert it into dictionary. 
            clase = output_dictionary["prediction"] # this dictionary will have clase (cat or not) y score (probability)
            score = output_dictionary["score"]
            db.delete(job_id) #when ready delete the id so as not to have info using space
            break


        # Don't forget to delete the job from Redis after we get the results!
        # Then exit the loop
        # TODO

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)

    return clase, score

import  time
import  redis
import  settings
import  uuid         # this is to generate a Universal Unique Identifier
import  json         # esto es para usar los comandos que transforman json

# TODO

db = redis.Redis(       
    host = settings.REDIS_IP, 
    port = settings.REDIS_PORT, 
    db   = settings.REDIS_DB_ID,
)

# Connect to Redis
#if condition returns False, AssertionError is raised:
db.ping()
# assert db.ping(), "I couldnt connect"


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
    
    # Assign an unique ID for this job:
    job_id = str(uuid.uuid4())
    
    job_data = {
        "id": job_id,
        "image_name": image_name,
    }
           
    # Send the job to the model service using Redis
    # Hint: Using Redis `rpush()` function should be enough to accomplish this.
    
    # con rpush ya entra al modelo
    db.rpush(settings.REDIS_QUEUE, json.dumps(job_data)) # lo transformamos json porque redis solo acepta strings
    
    # Loop until we received the response from our ML model
    while True:
        # Attempt to get model predictions using job_id
        # Hint: Investigate how can we get a value using a key from Redis
        
        if (db.exists(job_id)): #si existe este id
            # con get obtengo el resultado del modelo
            output            = db.get(job_id)
            output            = json.loads(output) 
            # este diccionario tiene tipo de clase y score
            
            clase             = output['class_name'] 
            score             = output['score']
            # Don't forget to delete the job from Redis after we get the results!
        
            db.delete(job_id)
            # Then exit the loop
        
        break 
        
        

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)

    return clase, score

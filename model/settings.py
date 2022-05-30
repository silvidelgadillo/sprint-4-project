import os

# We will store images uploaded by the user on this folder
UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# REDIS
# Queue name
REDIS_QUEUE = "job"
# Port
REDIS_PORT = 6379
# DB Id (ramdom)
REDIS_DB_ID = 0
# Host IP (choose by us)
REDIS_IP = "redis"
# Sleep parameters which manages the
# interval between requests to our redis queue
API_SLEEP = 0.05

import os

# Run API in Debug mode
API_DEBUG = True

# We will store images uploaded by the user on this folder
UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# We will store user feedback on this file
FEEDBACK_FILEPATH = "feedback/feedback"
os.makedirs(os.path.basename(FEEDBACK_FILEPATH), exist_ok=True)

# REDIS settings
# Queue name
REDIS_QUEUE = 'job' # cualquier numero pero debe ser igual para model y api
# Port
REDIS_PORT = 6379
# DB Id
REDIS_DB_ID = 0 # cualquier numero pero debe ser igual para model y api
# Host IP
REDIS_IP = 'redis' # 0.0.0.0 es la ip loopback local de redis
# Sleep parameters which manages the
# interval between requests to our redis queue
API_SLEEP = 0.05

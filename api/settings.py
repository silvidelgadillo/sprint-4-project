# settings for REDIS

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
# Queue name (sayd in class)
REDIS_QUEUE = "job"
# Port
REDIS_PORT = 6379
# DB Id (ramdom hasta 20)
REDIS_DB_ID = 0
# Host IP (choose by us)
REDIS_IP = "redis"
# Sleep parameters which manages the
# interval between requests to our redis queue
API_SLEEP = 0.05

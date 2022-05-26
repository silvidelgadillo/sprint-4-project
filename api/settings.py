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
REDIS_QUEUE = None
# Port
REDIS_PORT = None
# DB Id
REDIS_DB_ID = None
# Host IP
REDIS_IP = None
# Sleep parameters which manages the
# interval between requests to our redis queue
API_SLEEP = 0.05

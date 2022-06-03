import os

# Run API in Debug mode
API_DEBUG = True

# We will store images uploaded by the user on this folder
UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# We will store user feedback on this file
# FEEDBACK_FILEPATH = "feedback/feedback"
FEEDBACK_FILEPATH = "feedback/feedback.csv"
# os.stat(FEEDBACK_FILEPATH)
# Change basename to dirname to use first part, not the second with .csv
os.makedirs(os.path.dirname(FEEDBACK_FILEPATH), exist_ok=True)

# REDIS settings
# Queue name
REDIS_QUEUE = "job"
# Port
REDIS_PORT = 6379
# DB Id
REDIS_DB_ID = 1 #use the same in api and model
# Host IP
REDIS_IP = "sprint-4-project_redis_1" # redis / 0.0.0.0 / localhost / sprint-4-project_redis_1
# Sleep parameters which manages the
# interval between requests to our redis queue
API_SLEEP = 0.05
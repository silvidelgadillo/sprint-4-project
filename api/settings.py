import os

# Run API in Debug mode
API_DEBUG = True

# We will store images uploaded by the user on this folder
UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# uploads de carpeta raíz, static/ se escribe así porque si

# Limit the file weight to 16 MB
MAX_CONTENT_LENGTH = 16 * 1000 * 1000

# We will store user feedback on this file
FEEDBACK_FILEPATH = "feedback/feedback"
os.makedirs(os.path.basename(FEEDBACK_FILEPATH), exist_ok=True)
# idem upload

# REDIS settings
# Queue name
REDIS_QUEUE = "job"
# Port
REDIS_PORT = 6379
# DB Id
REDIS_DB_ID = 0
# Host IP
REDIS_HOST_NAME = "sprint-4-project_redis_1"
# Sleep parameters which manages the
# interval between requests to our redis queue
API_SLEEP = 0.05

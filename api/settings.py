import os

# It has all the API settings

# El módulo de SO en Python proporciona funciones para interactuar 
# con el sistema operativo como crear una carpeta,
# listar contenidos de una carpeta, 
# conocer acerca de un proceso, finalizar un proceso, etc

# Todas las funciones en el módulo del sistema operativo 
# generan OSError en el caso de nombres y rutas de archivo 
# no válidos o inaccesibles, u otros argumentos 
# que tienen el tipo correcto pero que el sistema operativo no acepta. 


# Run API in Debug mode
API_DEBUG = True

# We will store images uploaded by the user on this folder
UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# We will store user feedback on this file
FEEDBACK_FILEPATH = "feedback/feedback"
os.makedirs(os.path.basename(FEEDBACK_FILEPATH), exist_ok=True)

# os.path.basename : Returns the final component of a pathname

# El método os.makedirs() en Python se usa para crear un 
# directorio de forma recursiva. Eso significa que mientras 
# crea un directorio hoja si falta algún
# directorio de nivel intermedio, el método os.makedirs() los creará todos



# REDIS settings
# Queue name
REDIS_QUEUE = "app_queue"
# Port
REDIS_PORT = 6379
# DB Id
REDIS_DB_ID = 0
# Host IP
REDIS_IP = "redis"
# Sleep parameters which manages the
# interval between requests to our redis queue
API_SLEEP = 0.05

from fileinput import filename
import utils # módulo de la api
import settings # módulo de la api
import middleware # módulo de la api
import os

# Contains the API endpoints
# Los endpoints son las URLs de un API o un backend que responden a una petición.
# Una petición HTTP que retorna JSON

from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

# la comunicación entre clientes y el servidores en Internet, 
# se realizan a través del protocolo HTTP (Protocolo de Transferencia de Hipertexto). 
# Un usuario envía una solicitud a un servidor, 
# el cual da como respuesta una pagina web (un documento HTML). Los métodos
# utilizados para este tipo de comunicación son los parámetros GET y POST.

# GET & POST
# GET : envía la información haciéndola visible en la URL de la pagina web
# ej: https://www.pythondiario.com/articulos.html?tag=Flask
# uso: GET para la configuración de páginas web(filtros, ordenación, búsquedas, etc.)

# POST: envía la información ocultándola del usuario 
# (adjunta datos al organismo solicitado)
# ej: https://www.pythondiario.com/articulos.html
# uso: POST para la transferencia de información y datos.

router = Blueprint("app_router", __name__, template_folder="templates")

# get() recibe como parametro lo que queremos recuperar
@router.route("/", methods=["GET"]) # indica la ruta a seguir y el metodo
def index():
    """
    Index endpoint, renders our HTML code.
    """
    return render_template("index.html") # renderizar un template con un formulario


@router.route("/", methods=["POST"])
def upload_image():
    """
    Function used in our frontend so we can upload and show an image.
    When it receives an Uimage from the UI, it also calls our ML model to
    get and display the predictions.
    UI:(interfaz de usuario) es el conjunto de elementos de la pantalla 
    que permiten al usuario interactuar con una página web
    """
# REQUEST
# To access incoming request data, you can use the global request object. 
# Flask parses incoming request data
# for you and gives you access to it through that global object.
# The request object is an instance of a Request  
    
    # No file received, show basic UI
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    # File received but no filename is provided, show basic UI
    file = request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect(request.url)
# Flashes a message to the next request. In order to remove the flashed message
# from the session and to display it to the user, 
# the template has to call get_flashed_messages (SE USA EN HTML)


    # File received and it's an image, we must show it and get predictions
    if file and utils.allowed_file(file.filename):
        # In order to correctly display the image in the UI and get model
        # predictions you should implement the following:
        #   1. Get an unique file name using utils.get_file_hash() function
        #   2. Store the image to disk using the new name
        #   3. Send the file to be processed by the `model` service
        #      Hint: Use middleware.model_predict() for sending jobs to model
        #            service using Redis.
        #   4. Update `context` dict with the corresponding values
        
        file_name = utils.get_file_hash(file) # 1
        file.save(os.path.join(settings.UPLOAD_FOLDER, file_name)) # 2 
        # Join two or more pathname components, inserting '/' as needed. 
        # If any component is an absolute path, all previous 
        # path components will be discarded.
        # An empty last part will result in a path that ends with a separator

        predict, score = middleware.model_predict(file_name) # 3
        context = {  # 4
            "prediction": predict,
            "score": score,
            "filename": file_name,
        }
        
        # Update `render_template()` parameters as needed
    
        return render_template(
            "index.html", filename=file_name, context=context
        )
    # File received and but it isn't an image
    else:
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return redirect(request.url)

# para indicar a Flask qué URL debe activar nuestra función
@router.route("/display/<filename>")
def display_image(filename):
    """
    Display uploaded image in our UI.
    """
    return redirect(
        url_for("static", filename="uploads/" + filename), code=301
    ) # Generates a URL to the given endpoint with the method provided.

# Códigos de estado de respuesta HTTP
# Respuestas informativas (100–199),
# Respuestas satisfactorias (200–299),
# Redirecciones (300–399),
# Errores de los clientes (400–499),
# Errores de los servidores (500–599).

# 301: Este código de respuesta significa que la URL  del 
# recurso solicitado ha sido cambiado. 
# Probablemente una nueva URL sea devuelta en la respuesta

@router.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint used to get predictions without need to access the UI.
                                    # esto significa que el method es POST
    Parameters
    ----------
    file : str
        Input image we want to get predictions from.

    Returns
    -------
    flask.Response
        JSON response from our API having the following format:
            {
                "success": bool,
                "prediction": str,
                "score": float,
            }

        - "success" will be True if the input file is valid and we get a
          prediction from our ML model.
        - "prediction" model predicted class as string.
        - "score" model confidence score for the predicted class as float.
    """
    # To correctly implement this endpoint you should:
    #   1. Check a file was sent and that file is an image
    #   2. Store the image to disk
    #   3. Send the file to be processed by the `model` service
    #      Hint: Use middleware.model_predict() for sending jobs to model
    #            service using Redis.
    #   4. Update and return `rpse` dict with the corresponding values
    # If user sends an invalid request (e.g. no file provided) this endpoint
    # should return `rpse` dict with default values HTTP 400 Bad Request code
    
    file = request.files["file"]
    if file and utils.allowed_file(file.filename): # 1
        file.save(os.path.join(settings.UPLOAD_FOLDER, filename)) # 2 
    prediction, score = middleware.model_predict(file) # 3
    rpse = {"success": True, "prediction": {prediction}, "score": {score}} # 4

    return jsonify(rpse), 400

@router.route("/feedback", methods=["GET", "POST"])
def feedback():
    """
    Store feedback from users about wrong predictions on a text file.

    Parameters
    ----------
    report : request.form
        Feedback given by the user with the following JSON format:
            {
                "filename": str,
                "prediction": str,
                "score": float
            }

        - "filename" corresponds to the image used stored in the uploads
          folder.
        - "prediction" is the model predicted class as string reported as
          incorrect.
        - "score" model confidence score for the predicted class as float.
    """
    # Get reported predictions from `report` key
    report = request.form.get("report")

    # Store the reported data to a file on the corresponding path
    # already provided in settings.py module

    
    if report:
    # 'a': opens a file for appending at the end of the 
    # file without truncating it. Creates a new file if it does not exist.
        with open(settings.FEEDBACK_FILEPATH, "a") as feedback:
    # write: used to write into a file using the file object
            report = feedback.write(f'Report:{report}/n')
            
    return render_template("index.html")
    



# FLASK RESPONSE
# El objeto de respuesta que se usa de forma predeterminada en Flask
# está configurado para tener un tipo MIME de HTML de forma predeterminada
# MIME: El tipo Extensiones multipropósito de Correo de Internet (MIME) 
# es una forma estandarizada de indicar 
# la naturaleza y el formato de un documento, archivo o conjunto de datos.
# La estructura de un tipo MIME es muy simple; 
# consiste en un tipo y un subtipo, dos cadenas, separadas por un '/'.
# tipo/subtipo
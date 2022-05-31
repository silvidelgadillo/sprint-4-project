## so as everything done here brings the utils we define previously
from asyncio import FastChildWatcher

import utils
import os
import os.path
import settings
from middleware import model_predict
from utils import get_file_hash
import json

## views = different endpoints of the API
## flask is the background to code in API
## blueprint --> divide the code
## flash --> print
## redirect --> navigate inside API
## request --> ask the API something but positioning in the endpoint
## url --> returns the route of the transaction made

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify
)

## here we inicialize the API

router = Blueprint("app_router", __name__, template_folder="templates")


## define the endpoints (index, upload image, display image, predict, playback, feedback)

@router.route("/", methods=["GET"])
def index():
    """
    Index endpoint, renders our HTML code.
    """
    return render_template("index.html")




@router.route("/", methods=["POST"])
def upload_image():
    """
    Function used in our frontend so we can upload and show an image.
    When it receives an image from the UI, it also calls our ML model to
    get and display the predictions.
    """
    # No file received, show basic User Interface
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    # File received but no filename is provided, show basic UI
    file = request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect(request.url)

    # File received and it's an image, we must show it and get predictions
    if file and utils.allowed_file(file.filename):
        # In order to correctly display the image in the UI and get model
        # predictions you should implement the following:
        
        #   1. Get an unique file name using utils.get_file_hash() function
        # Here we define the variable with the utils function "get file hash" we define in utils.py
        new_file = utils.get_file_hash(file)
        
        #   2. Store the image to disk using the new name
        ## store image (os.path so as not to replace images if they are the same)
        ## if path does not exist creat a new one
        ## check it out: https://www.geeksforgeeks.org/python-os-path-lexists-method/
        #if os.path.lexists(new_file.path) == False:            
        #file.save(os.path.join(file, new_file))
        file.save(os.path.join(settings.UPLOAD_FOLDER, new_file))


        #   3. Send the file to be processed by the `model` service
        #      Hint: Use middleware.model_predict() for sending jobs to model
        #            service using Redis.

        predict, score = model_predict(new_file)

        #   4. Update `context` dict with the corresponding values
        ## context values of dictionary are actualized

        context = {"prediction": predict, "score": round(score,4), "filename": new_file}

        # Update `render_template()` parameters as needed
        return render_template("index.html", filename = new_file, context = context)
    # File received and but it isn't an image
    else:
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return redirect(request.url)




@router.route("/display/<filename>")
def display_image(filename):
    """
    Display uploaded image in our UI.
    """
    return redirect(url_for("static", filename="uploads/" + filename), code=301)


@router.route("/predict", methods=["POST"])
def predict():
    ## predict when the file is out of UI
    """
    Endpoint used to get predictions without need to access the UI.

    Parameters
    ----------
    file : str
        Input image we want to get predictions from.

    Returns
    -------
    flask.Response
        JSON (JAVA Language) response from our API having the following format:
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
    #   1. Check a file was sent and that file is an image and conditions are accomplished

    correct_file = "file" in request.files and \
                    request.files["file"] is not None and \
                    utils.allowed_file(request.files["file"].filename)
    
    ## if conditions are accomplished correctly:
    if correct_file:
        
    #   2. Rename the file (hasheando) and Store the image to disk
    ## define File, new_file and the path where I wanted to save it
        file = request.files["file"]
        new_file = utils.get_file_hash(file)

        file_path = settings.UPLOAD_FOLDER + new_file

    ## if the path does not exits save it into the one we are using
        if not os.path.exists(file_path):
            file.save(file_path)
            file.close()
        
    #   3. Send the file to be processed by the `model` service
    #      Hint: Use middleware.model_predict() for sending jobs to model
    #            service using Redis.

        ## if condictions are accomplished, do this: predict it
        predict, score = model_predict(new_file)
      
    #   4. Update and return `rpse` dict with the corresponding values
    # If user sends an invalid request (e.g. no file provided) this endpoint
    # should return `rpse` dict with default values HTTP 400 Bad Request code
    # rpse = {"success": False, "prediction": None, "score": None}

        rpse = {"success": True, "prediction": predict, "score": round(score,4)}
        
        ## return this response (RSPE) in jason format
        return jsonify(rpse), 200
    
    else:
        rpse = {"success": False, "prediction": None, "score": None}
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
        with open(settings.FEEDBACK_FILEPATH,"a+") as file2:
            file2.write(report+'\n')  #\n is used to read file in a nice way

    return render_template("index.html")

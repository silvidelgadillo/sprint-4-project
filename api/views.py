import utils
import middleware
import settings
import os
import json

from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
    Response,
)
from middleware import model_predict

router = Blueprint("app_router", __name__, template_folder="templates")

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
    # No file received, show basic UI
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
        # TODO
        # 1. Get an unique file name using utils.get_file_hash() function
        uniqueName = utils.get_file_hash(file)
        # os.rename(file.filename, uniqueName)
        # 2. Store the image to disk using the new name
        path = os.path.join(settings.UPLOAD_FOLDER, uniqueName)
        if not os.path.exists(path):
            file.save(path)
        # 3. Send the file to be processed by the `model` service
        result = middleware.model_predict(uniqueName)
        # 4. Update `context` dict with the corresponding values
        context = {
            "prediction": result[0],
            "score": result[1],
            "filename": uniqueName,
        }

        # Update `render_template()` parameters as needed
        # TODO
        return render_template(
            "index.html", filename=uniqueName, context=context
        )
    # File received and but it isn't an image
    else:
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return redirect(request.url)


@router.route("/display/<filename>")
def display_image(filename):
    """
    Display uploaded image in our UI.
    """
    return redirect(
        url_for("static", filename="uploads/" + filename), code=301
    )


@router.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint used to get predictions without need to access the UI.

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
    # TODO
    # 1. Check a file was sent and that file is an image
    # file_exists = ("file" in request.files)
    # file_not_null = (request.files["file"] is not None)
    # return jsonify({"success": False, "prediction": None, "score": None}), 400
    # file_is_allowed = (utils.allowed_file(request.files["file"].filename))
    #if (file in request.files) and (utils.allowed_file(file.filename)):
    if "file" in request.files:
        file = request.files["file"]
        if file and utils.allowed_file(file.filename):
            # 2. Store the image to disk
            uniqueName = utils.get_file_hash(file)
            path = os.path.join(settings.UPLOAD_FOLDER, uniqueName)
            if not os.path.exists(path):
                file.save(path)
            # 3. Send the file to be processed by the `model` service
            #    Use middleware.model_predict() for sending jobs to model service using Redis.
            result = model_predict(uniqueName)
            # 4. Update and return `rpse` dict with the corresponding values
            # If user sends an invalid request (e.g. no file provided) this endpoint
            # should return `rpse` dict with default values HTTP 400 Bad Request code
            rpse = {"success": True, "prediction": result[0], "score": result[1]}
            return jsonify(rpse), 200
    
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
    # TODO
    if report:
        with open(settings.FEEDBACK_FILEPATH, "a+") as f:
            f.write(report + "\n")

    return render_template("index.html")
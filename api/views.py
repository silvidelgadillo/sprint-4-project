import utils
import settings
import os
import middleware
import csv

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

router = Blueprint("app_router", __name__, template_folder="templates")

# GET method in order to render template for first time.
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
        unique_file_name = utils.get_file_hash(file)
        path = os.path.join(settings.UPLOAD_FOLDER, unique_file_name)
        if not os.path.exists(path):
            file.save(path)

        context = {
            "prediction": None,
            "score": None,
            "filename": None,
        }
        results = middleware.model_predict(unique_file_name)
        context.update({"prediction": results[0],
                        "score": results[1],
                        "filename": unique_file_name})

        return render_template("index.html", filename=unique_file_name, context=context)

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
    #   1. Check a file was sent and that file is an image
    #   2. Store the image to disk
    #   3. Send the file to be processed by the `model` service
    #      Hint: Use middleware.model_predict() for sending jobs to model
    #            service using Redis.
    #   4. Update and return `rpse` dict with the corresponding values
    # If user sends an invalid request (e.g. no file provided) this endpoint
    # should return `rpse` dict with default values HTTP 400 Bad Request code
    # TODO
    rpse = {"success": False, "prediction": None, "score": None}


@router.route("/feedback", methods=["GET", "POST"])
def feedback():

    # Get reported predictions from `report` key
    report = request.form.get("report")
    
    fb_path = os.path.join(settings.FEEDBACK_FILEPATH, '/feedback.csv')
    if not os.path.exists(fb_path):
        with open(fb_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter= ',')
            writer.writerow(['Filename', 'Prediction', 'Score'])
            writer.writerow(report)
        file.close()
        flash('Thank you for your feedback!')
    else:
        with open(fb_path, 'a') as file:
            file.write(report)
        file.close()
        flash('Thank you for your feedback!')
        
    return render_template("index.html")

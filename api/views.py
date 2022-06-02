import sys
import os
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import ValidationError
import utils
import middleware

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    current_app
)

images_set = UploadSet('images', IMAGES)

def my_filename_not_empty_check(msg):
    def _my_filename_not_empty_check(form, field):
        if len(field.data.filename) <= 0:
            raise ValidationError(msg)
    return _my_filename_not_empty_check

def my_allowed_fileextension_check(msg):
    def _my_allowed_fileextension_check(form, field):
        if utils.allowed_file(field.data.filename) is False:
            raise ValidationError(msg)
    return _my_allowed_fileextension_check

class UploadForm(FlaskForm):
    image = FileField('image', validators=[
        FileRequired('No file part'),
        my_filename_not_empty_check("No image selected for uploading"),
        FileAllowed(images_set, "Only images allowed"),
        my_allowed_fileextension_check("Allowed image types are -> png, jpg, jpeg, gif")
    ])

router = Blueprint("app_router", __name__, template_folder="templates")


@router.route("/", methods=["GET"])
def index():
    """
    Index endpoint, renders our HTML code.
    """
    form = UploadForm()
    return render_template("index.html", form=form)


@router.route("/", methods=["POST"])
def upload_image():
    """
    Function used in our frontend so we can upload and show an image.
    When it receives an image from the UI, it also calls our ML model to
    get and display the predictions.
    """
    print('Entering upload_image')
    form = UploadForm()
    if form.validate_on_submit():
        f = form.image.data
        filename = secure_filename(f.filename)

        # File received and it's an image, we must show it and get predictions

        # In order to correctly display the image in the UI and get model
        # predictions you should implement the following:
        #   1. Get an unique file name using utils.get_file_hash() function
        uploaded_file = request.files['image']
        hashed_filename = utils.get_file_hash(uploaded_file)
        #   2. Store the image to disk using the new name
        uploaded_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], hashed_filename))
        #   3. Send the file to be processed by the `model` service
        #      Hint: Use middleware.model_predict() for sending jobs to model
        #            service using Redis.
        prediction, score = middleware.model_predict(hashed_filename)
        #   4. Update `context` dict with the corresponding values
        context = {
            "prediction": prediction,
            "score": score,
            "filename": hashed_filename,
        }

        # Update `render_template()` parameters as needed
        print('success: Returning from upload_image')
        return render_template(
            "index.html", filename=hashed_filename, context=context, form=form
        )
    else:
        utils.flash_errors(form)
    
    return render_template("index.html", form=form)


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

    return render_template("index.html")

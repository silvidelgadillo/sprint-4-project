import utils
from middleware import model_predict
import settings
import json
from os import path

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    make_response,
)

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

        hash_imgname = utils.get_file_hash(file)
        img_savepath = path.join(settings.UPLOAD_FOLDER, hash_imgname)

        if not path.exists(img_savepath):  # Check if the file already exist
            file.stream.seek(0)
            file.save(img_savepath)

        prediction, score = model_predict(hash_imgname)

        context = {
            "prediction": utils.get_hr_class(prediction),
            "score": score,
            "filename": hash_imgname,
        }

        return render_template("index.html", filename=hash_imgname, context=context)

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

    error_rpse = {"success": False, "prediction": None, "score": None}
    error_rspe_str = json.dumps(error_rpse)
    error_response = make_response(error_rspe_str)
    error_response.status_code = 400

    # No file received, show basic UI
    if "file" not in request.files:
        return error_response

    # File received but no filename is provided
    file = request.files["file"]
    if file.filename == "":
        rpse = {"success": False, "prediction": None, "score": None}
        return error_response

    # File received and it's an image
    if file and utils.allowed_file(file.filename):

        hash_imgname = utils.get_file_hash(file)
        img_savepath = path.join(settings.UPLOAD_FOLDER, hash_imgname)

        if not path.exists(img_savepath):  # Check if the file already exist
            file.stream.seek(0)
            file.save(img_savepath)

        prediction, score = model_predict(hash_imgname)

        rpse = {"success": True, "prediction": prediction, "score": score}

        rpse_str = json.dumps(rpse)

        response = make_response(rpse_str)
        response.status_code = 200

        return response

    # File received and but it isn't an image
    else:
        return error_response


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
    # Get reported predictions from `report` key
    report = request.form.get("report")

    with open(f"{settings.FEEDBACK_FILEPATH}", "a") as f:
        f.write(f"{report}\n")

    return render_template("index.html")

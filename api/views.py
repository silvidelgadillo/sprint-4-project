import utils
from middleware import model_predict
import settings

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify
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
    # process file
    result = utils.process_file(request, "file")

    file_name = result['file_name']

    if not result['valid']:
        flash(result['error'])
        context = None
        if(result['redirect_home']):
            return redirect(request.url)
    else:
        # In order to correctly display the image in the UI and get model
        # predictions you should implement the following:
        #   1. Get an unique file name using utils.get_file_hash() function
        #   2. Store the image to disk using the new name
        #   3. Send the file to be processed by the `model` service
        #      Hint: Use middleware.model_predict() for sending jobs to model
        #            service using Redis.
        #   4. Update `context` dict with the corresponding values

        class_name, score = model_predict(file_name)

        context = {
            "prediction": class_name,
            "score": score,
            "filename": file_name,
        }

    # Update `render_template()` parameters as needed
    return render_template(
        "index.html", filename=file_name, context=context
    )


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
    # 

    # process file
    result = utils.process_file(request, "file")

    if not result['valid']:
        rpse = {"success": False, "prediction": None, "score": None}
        # if required by the frontpage
        if ('front' in request.form):
            rpse['error'] = result['error']
        return jsonify(rpse), 400

    file_name = result['file_name']

    class_name, score = model_predict(file_name)

    rpse = {"success": True, "prediction": class_name, "score": score}

    # if required by the frontpage
    if ('front' in request.form):
        rpse['file_name'] = file_name
        
    return jsonify(rpse)


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

    if(report):
        with open(settings.FEEDBACK_FILEPATH, "a") as feedback:
            # Append feedback at the end of file
            feedback.write(str(report) + "\n")

    # if required by the frontpage
    if ('front' in request.form):
        return '1'

    return render_template("index.html")

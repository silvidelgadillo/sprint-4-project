import utils
import os
import app
import settings
from middleware import model_predict 

from flask import (
    jsonify,
    Blueprint, 
    flash,  
    redirect, 
    request, 
    url_for,
    render_template,
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
    
    if "file" not in request.files:  
        flash("No file part")
        return redirect(request.url) 

    file = request.files["file"] 
    if file.filename == "": 
        flash("No image selected for uploading")
        return redirect(request.url)

    if file and utils.allowed_file(file.filename):
        filename_hashed = utils.get_file_hash(file)
        loc_store_img = os.path.join(settings.UPLOAD_FOLDER, filename_hashed)

        if os.path.exists(loc_store_img) is False:
            file.save(loc_store_img) 

        pred, score = model_predict(filename_hashed)

        context = {
            "prediction": pred,
            "score": score,
            "filename": filename_hashed,
        }

        return render_template(
            "index.html", filename=filename_hashed, context=context     
        )

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
    """
    rpse = {"success": False, "prediction": None, "score": None}
    if "file" not in request.files:  
        return jsonify(rpse), 400

    file = request.files["file"] 
    if file.filename == "": 
        return jsonify(rpse), 400

    if file and utils.allowed_file(file.filename):
        filename_hashed = utils.get_file_hash(file)
        loc_store_img_0 = os.path.join(settings.UPLOAD_FOLDER, filename_hashed)

        if os.path.exists(loc_store_img_0) is False:
            file.save(loc_store_img_0)

        pred, sc = model_predict(filename_hashed) 

        rpse = {"success": True, "prediction": pred, "score": sc}
        return jsonify(rpse)
    else:
        rpse = {"success": False, "prediction": None, "score": None}
        return jsonify(rpse)     

@router.route("/feedback", methods=["GET", "POST"])
def feedback():
    """
    Store feedback from users about wrong predictions on a text file.
    """
    
    report = request.form.get("report")
    feedback_file = open(str(settings.FEEDBACK_FILEPATH), "a")
    feedback_file.write(str(report) + "\n")

    return render_template("index.html")

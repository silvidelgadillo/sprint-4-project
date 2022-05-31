import settings
from flask import Flask
from views import router
from flask_uploads import configure_uploads
from views import images_set

### Application Factory ###
def create_app():

    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = settings.UPLOAD_FOLDER
    app.config["UPLOADED_IMAGES_DEST"] = settings.UPLOAD_FOLDER
    app.secret_key = "secret key"
    app.register_blueprint(router)
    configure_uploads(app, images_set)

    return app

app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=settings.API_DEBUG)

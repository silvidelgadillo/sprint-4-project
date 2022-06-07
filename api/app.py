import settings
from flask import Flask
from views import router
from flask_uploads import configure_uploads
from views import images_set
from flask_wtf.csrf import CSRFProtect

### Application Factory ###
def create_app():

    app = Flask(__name__)
    csrf = CSRFProtect(app)
    app.config["UPLOAD_FOLDER"] = settings.UPLOAD_FOLDER
    app.config["UPLOADED_IMAGES_DEST"] = settings.UPLOAD_FOLDER
    app.secret_key = "secret key"
    app.register_blueprint(router)
    configure_uploads(app, images_set)
    csrf.init_app(app)
    #csrf.exempt(router)
    #app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    app.config['WTF_CSRF_ENABLED'] = False # TODO: Temporary workaround. Should instead remove csrf protection only when necessary.

    return app

app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=settings.API_DEBUG)

import settings
from flask import Flask # flask subrayado en amarillo. Pablo: "es porque no estoy en el entorno"
from views import router

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = settings.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = settings.MAX_CONTENT_LENGTH
app.secret_key = "secret key"
app.register_blueprint(router)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=settings.API_DEBUG)
    
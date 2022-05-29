import settings # se importa un archivo dentro de sprint-4-project
from flask import Flask
from views import router

# FIRST STEP: CREATE THE APP WITH FLASK
# app
app = Flask(__name__)
# configuration the folder to save the image upload
app.config["UPLOAD_FOLDER"] = settings.UPLOAD_FOLDER
# this is a secret key that is used by Flask to sign cookies
app.secret_key = "secret key"

# blueprint se utiliza para organizar la aplicacion en distintos módulos
# ya sea de manera funcional o estructural
# primero se importa (esta importado con Flask) 
# y luego se registra en la app como en el sig paso
app.register_blueprint(router) # router es un decorador

# DECORADORES:
# Los decoradores forman parte de un patrón de diseño, el cual permite al 
# usuario añadirle funcionalidad a un objeto (método o función) 
# sin modificar su estructura interna

# Inicializando la app
# Runs the application on a local development server
if __name__ == "__main__": # esto garantiza que el metodo run() se llame solo 
                           # cuando se ejecute el archivo principal
    app.run(host="0.0.0.0", debug=settings.API_DEBUG)

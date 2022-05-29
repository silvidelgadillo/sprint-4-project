FROM python:3.8.13 as base

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/src/

ADD ./ /src/

WORKDIR /src

FROM base as test
RUN ["pytest", "-v", "/src/tests"]

FROM base as build
ENTRYPOINT ["gunicorn", "--workers=8", "--bind", "0.0.0.0:5000", "app:app"]


# Un DockerFile es un documento de texto que 
# contiene todos los comandos que queramos 
# ejecutar en la linea de comandos para armar una imágen. 
# Esta imágen se creará mediante el comando docker build 
# que irá siguiendo las instrucciones.

# comando: docker-compose up --build
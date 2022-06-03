Introdiction:
This project is based on two trunk axes: api and model. We are going to build and run three cointainers, each one with their own image. This is set up 1) at the docker-comppose file and then in each foler (dockerfile). 
Also, each folder have their own requirement and settings.

API:
    - The main api file is views. In wich all the endpoints are defined and implemented. Another file is utils were we implement the function to check if the file have the corresponding extension and another function that hash the file. Finaly the middleware file its the one that comunicate with Redis and the model. 

Model:
    - Basically ml_service is the main file from this part. In wich we implement and call the model. In this case we use an already trained model.
    
Versioning:     
1) Utility function completed and tested.

2) Views--> upload_image(), so I needed to complete middleware first.
    - 1) learn about Redis. 
    - 2) I set up a fake model who always return the same values.
once everithing works I finished the upload_image function.

3) model_service 
    - 1) with a fake model
    - 2) with the actual model.  There are some tricks like: image size, data_type (pillow), and to get the one with the highest probability. 

4) views --> predict()

5) Feedback

Test: 

    1) Testing utility function.
    2) Testing predict and feedback.
    3) Integration testing.
    4) Testing predict using postman and it works
    5) stress_test: install and understand locust. See Anexo1
    6) stress_test: with a scalled model. I count with a 4C AMD-A10. RAM = 16G. See Anexo2.


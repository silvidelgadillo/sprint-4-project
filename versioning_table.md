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

Test: I think that the hardest thing for me was to find a way to passed the predict()



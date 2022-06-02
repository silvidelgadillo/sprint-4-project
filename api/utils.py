import os
import hashlib
import settings

def allowed_file(filename):
    """
    Checks if the format for the file received is acceptable. For this
    particular case, we must accept only image files.

    Parameters
    ----------
    filename : str
        Filename from werkzeug.datastructures.FileStorage file.

    Returns
    -------
    bool
        True if the file is an image, False otherwise.
    """

    split_file = os.path.splitext(filename)
    return str(split_file[1]).lower() in [".gif", ".jpeg", ".jpg", ".png"]


def get_file_hash(file):
    """
    Returns a new filename based on the file content using MD5 hashing.
    It uses hashlib.md5() function from Python standard library to get
    the hash.

    Parameters
    ----------
    file : werkzeug.datastructures.FileStorage
        File sent by user.

    Returns
    -------
    str
        New filename based in md5 file hash.
    """
    
    split_file = os.path.splitext(file.filename)
    data = file.read()
    md5hash = hashlib.md5(data).hexdigest()
    file.seek(0)

    return str(md5hash) + str(split_file[1])

def process_file(request, file_request):

    # No file received, show basic UI
    if file_request not in request.files:
        return {'error': "No file part", 
                'redirect_home': True, 
                'valid': False, 'file_name': False}

    # File received but no filename is provided, show basic UI
    file = request.files[file_request]
    if file.filename == "":
        return {'error': "No image selected for uploading", 
                'redirect_home': True, 
                'valid': False,
                'file_name': False}
    
    if file and allowed_file(file.filename):
        file_name = get_file_hash(file)
        
        # if file not exist save it
        if(not os.path.exists(os.path.join(settings.UPLOAD_FOLDER, file_name))):
            file.save(os.path.join(settings.UPLOAD_FOLDER, file_name))

        return {'error': None, 'redirect_home': False, 'valid': True, 'file_name': file_name}
    
    return {'error': 'Allowed image types are -> png, jpg, jpeg, gif', 
            'redirect_home': False, 'valid': False, 'file_name': False}
    
def savePredictions(file_name, score, prediction):
    root_name, _ = os.path.splitext(file_name)
    file_name_txt = root_name + '.txt'
    if(not os.path.exists(os.path.join(settings.UPLOAD_FOLDER, file_name_txt))):
        with open(os.path.join(settings.UPLOAD_FOLDER, file_name_txt), "w") as prediction_file:
            prediction_file.write(prediction + "," + str(score)) 

def readPredictionFile(file_name):
    root_name, _ = os.path.splitext(file_name)
    file_name_txt = root_name + '.txt'
    if(os.path.exists(os.path.join(settings.UPLOAD_FOLDER, file_name_txt))):
        with open(os.path.join(settings.UPLOAD_FOLDER, file_name_txt), "r") as prediction_file:
            class_name, score = prediction_file.read().split(",")
        return class_name, float(score)
    return False, False
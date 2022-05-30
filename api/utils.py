from hashlib import md5
from os.path import splitext
import json

ALLOWED_IMG_EXT = {".png", ".jpg", ".jpeg", ".gif"}

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
    
    _, ext = splitext(filename)
    ext = ext.lower()

    valid_file = ext in ALLOWED_IMG_EXT
    
    return valid_file


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
    
    _, ext = splitext(file.filename)
    readable_hash = md5(file.read()).hexdigest() 
    hash_filename = f"{readable_hash}{ext}"
    file.stream.seek(0)

    return hash_filename

def get_hr_class(classname):
    """
    Map the class name output from the model to a human readable class name 
    to show in the front-end.

    Parameters
    ----------
    class_name : str
        Output from the model.

    Returns
    -------
    str
        Human readable class name.
    """
    
    with open("./classes_map.json", "r") as f:
        classes_map = json.load(f)
    
    return classes_map[classname]

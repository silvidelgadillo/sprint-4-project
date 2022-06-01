import os
import hashlib

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
    # READ & DELETE
    # https://werkzeug.palletsprojects.com/en/1.0.x/datastructures/#werkzeug.datastructures.FileStorage
    # https://tedboy.github.io/flask/generated/generated/werkzeug.FileStorage.html

    ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif"}
    file_ext = os.path.splitext(filename)[1].lower() # return two variables

    if file_ext in ALLOWED_EXTENSIONS:
        check_allowed_file = True
    else:
        check_allowed_file = False

    return check_allowed_file
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
    file_hash = hashlib.md5(file.read()).hexdigest()
    _ , file_ext = os.path.splitext(file.filename)
    file_ext = file_ext.lower()
    file_hash_name = f'{file_hash}{file_ext}'
    file.seek(0) # return memory pointer to genesis
    
    return file_hash_name
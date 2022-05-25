from hashlib import md5
from os.path import splitext

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

    return hash_filename
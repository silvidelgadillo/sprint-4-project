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
    # Current implementation will allow any kind of file.
    ## here we define the acepted extentions, and separate name from extention
    ## then define lower letters in extention
    ## define valid file as allowed extentions only
    
    # TODO
    ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif"}
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    valid_file = ext in ALLOWED_EXTENSIONS
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

    ## encriptar el archivo
    ## import hashlib libreria with method md5 that brings a type of encryptation
    ## encripte the file by reading it first and translate it to something useful in sexadecimal (md5, read, hexdigest)
    ## as we need to return the file encripted and the extention of it, we call ext and then concatenate with var_hash
    ## file seek so as to start reading always from zero

    # Current implementation will return the original file name.
    # TODO
    var_hash = hashlib.md5(file.read()).hexdigest()
    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()
    var_filename = f'{var_hash}{ext}'
    file.seek(0)
    return var_filename
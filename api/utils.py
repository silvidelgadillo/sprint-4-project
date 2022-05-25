from dataclasses import asdict
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
    # Parameters > filename
    # https://werkzeug.palletsprojects.com/en/1.0.x/datastructures/#werkzeug.datastructures.FileStorage
    # https://tedboy.github.io/flask/generated/generated/werkzeug.FileStorage.html

    # ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    # si agrego un rfind > cuando no encuentra "." > devuelve -1 va directo a false
    # file_ext = filename.rsplit('.', 1)[1].lower() # troubles if not dot is found, like a path

    # check_filename = rfind(,)
    
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
    # Current implementation will return the original file name.
    # TODO

    # https://www.geeksforgeeks.org/md5-hash-python/
    # https://docs.python.org/3/library/hashlib.html
    # leer documentacion de fileStorege en weurkzaeug

    # ver de rescatar extension original
    # libreria imghdr
    # https://docs.python.org/3/library/imghdr.html

    file_hash = hashlib.md5(file.read()).hexdigest()
    _ , file_ext = os.path.splitext(file.filename)
    file_ext = file_ext.lower()
    file_hash_name = f'{file_hash}{file_ext}'
    file.seek(0) # vuelve puntero a inicio de memoria
    
    return file_hash_name

def save_file(file):
    """
    Returns a message confirmation after the file is saved.
    Could by "OK" or "ERROR" 

    Parameters
    ----------
    file : werkzeug.datastructures.FileStorage
        File sent by user.

    Returns
    -------
    str
        Confirmation message.
    """
    
    file_upload = file
    if file_upload == True:
        upload_msg_return = "OK"
    else: upload_msg_return = "ERROR"
    return upload_msg_return

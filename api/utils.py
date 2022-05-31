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
    # TODO

    allowed_ext = {".png", ".jpg", ".jpeg", ".gif"}

    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext in allowed_ext:
        return True
    else:
        return False 


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

    hash_name = hashlib.md5(file.read())
    ext = file.filename.rsplit('.',1)[1].lower()
    hashed_file = hash_name.hexdigest()+'.'+ext

    file.seek(0) # in order to return to first point in memory, so we can read it later

    return hashed_file
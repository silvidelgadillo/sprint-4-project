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
    ## Pablo´s answer
    # basename, ext = os.path.splitext(filename)
    # ext           = ext.lower()
    # valid_file    = ext in a

    # Current implementation will allow any kind of file.
    filename = str(filename).lower()
    VALID_FORMATS = {".png", ".jpg", ".jpeg", ".gif"}
    ### CHECK IT
    for i in VALID_FORMATS:
        msj = filename.endswith(i)

        if msj:
            return True
        else:
            pass
    if msj == False:
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
    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()

    # Current implementation will return the original file name.

    h = hashlib.md5(file.read())
    h = h.hexdigest()
    file.seek(0)

    new_name = f"{h}{ext}"
    return new_name

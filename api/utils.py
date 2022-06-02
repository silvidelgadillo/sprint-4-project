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
    # TODO
    allow_exts = {".png", ".jpg", ".jpeg", ".gif"}
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext in allow_exts:
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
    # TODO
    hash_file = hashlib.md5(file.read()).hexdigest()
    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()

    orig_file_name = f'{hash_file}{ext}'
    file.seek(0)

    return orig_file_name
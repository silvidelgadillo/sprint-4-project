import os
from flask import (
    flash,
)
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
    allowed_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    extension = os.path.splitext(filename)[-1].lower()
    return extension in allowed_extensions


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
    m = hashlib.md5()
    while len(chunk := file.stream.read(512)) != 0:
        m.update(chunk)
    file.stream.seek(0)
    
    return m.hexdigest() + os.path.splitext(file.filename)[-1]

def flash_errors(form):
    """
    Flashes form errors

    Parameters
    ----------
    form : flask_wtf.FlaskForm
        form handle which contains the errors to be flashed

    Returns
    -------
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

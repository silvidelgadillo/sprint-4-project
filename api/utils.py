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
    try:
        images_ext = {'.gif', '.jpeg', '.jpg', '.png'} #set para que sea mas rapido recorrerlo
        _, img_check = os.path.splitext(filename)    #como me devuelve un tupple ignoro la primer variable con _,
        img_check = img_check.lower()                  #todas las extensiones en minuscula

    except IOError:
        print("===========Error fetching file format")
    return img_check in images_ext


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
    _, split_file = os.path.splitext(file.filename)
    data = file.read()
    md5hash = hashlib.md5(data).hexdigest()
    file.seek(0)                #vuelvo el puntero para poder leerlo despues

    return str(md5hash) + str(split_file)
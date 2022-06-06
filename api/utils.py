from hashlib import md5

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
    if filename == None:
        return False

    exten = filename.split(".")[-1]

    return exten.lower() in {"png", "jpg", "jpeg", "gif"}


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

    hashed_file = md5(file.stream.read()).hexdigest()
    file.stream.seek(0)

    return f"{hashed_file}.jpeg"
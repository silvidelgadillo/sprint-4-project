import os
import hashlib #returns 128 bit hash value

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

    allowExt = {'.png', '.jpg', '.jpeg', '.gif'}

    split_tup = os.path.splitext(filename)

    file_extension = split_tup[1].lower()

    valid = file_extension in allowExt

    return valid


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

    content = file.read()
    # md5_hash = hashlib. md5()
    # md5_hash.update(content)

    # digest = md5_hash.hexdigest()

    newFilename = hashlib.md5(content).hexdigest()

    split_tup = os.path.splitext(file.filename)
    file_extension = split_tup[1].lower()

    hashFilename = newFilename + file_extension

    file.seek(0)

    # return os.path.basename(file.filename) // This is current implementation
    return hashFilename
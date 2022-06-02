import os
import hashlib

allowed_extensions = set([".png", ".jpg", ".jpeg", ".gif"])

def allowed_file(filename):
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext in allowed_extensions:
        return True
    else:
        return False
        

def get_file_hash(file):
    hash_file     = hashlib.md5(file.read()).hexdigest()
    _, ext        = os.path.splitext(file.filename)
    ext           = ext.lower()
    new_file_name = f"{hash_file}{ext}"
    file.seek(0) 

    return new_file_name
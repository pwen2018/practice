import hashlib


def encryptionMD5(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    md5_password = md5.hexdigest()
    return md5_password
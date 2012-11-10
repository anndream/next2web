import hashlib
import os

def md5sum(filename):
    if not os.path.exists(filename):
        raise ValueError, 'Unable to open file %s' % `filename`
    md5 = hashlib.md5()
    with open(filename) as f:
        for chunk in iter(lambda: f.read(125*md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()
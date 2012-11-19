import hashlib
import os
import locale
from gluon import current
import datetime, time

T = current.T
locale.setlocale(locale.LC_ALL, '')

def md5sum(filename):
    if not os.path.exists(filename):
        raise ValueError, 'Unable to open file %s' % `filename`
    md5 = hashlib.md5()
    with open(filename) as f:
        for chunk in iter(lambda: f.read(125*md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()

pretty = lambda txt: str(txt).lower().capitalize()

def safe_int(x):
    try:
        return int(x)
    except ValueError:
        return 0
    
def safe_float(x):
    try:
        return float(x)
    except ValueError:
        return 0.0

month_name = ['', T('Jan'), T('Feb'), T('Mar'), T('Abr'), T('May'), T('Jun'), T('Jul'), T('Ago'), T('Sep'), T('Oct'), T('Nov'), T('Dec')]
month_name_full = ['', T('January'), T('February'), T('March'), T('April'), T('May'), T('June'), T('August'), T('September'), T('Octuber'), T('November'), T('December')]

    
now = lambda: datetime.datetime.today()
today = lambda: datetime.date.today()
thistime = lambda: datetime.time(time.localtime()[3:7])

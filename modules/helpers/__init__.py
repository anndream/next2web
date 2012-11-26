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

def process_form(document, data):
    from field import fields
    vars, files = {}, {}
    for doc_field in document.META.DOC_FIELDS:
        if doc_field.df_type in fields and doc_field.df_type!='filelink' and hasattr(data, doc_field.df_name):
            vars[doc_field.df_name] = data[doc_field.df_name]
        if doc_field.df_type in fields and doc_field.df_type=='filelink' and hasattr(data, doc_field.df_name):
            vars[doc_field.df_name] = (data[doc_field.df_name].filename, data[doc_field].file)
    return (vars, files)

def temp_store_file(file_data):
    from tempfile import NamedTemporaryFile
    f = NamedTemporaryFile(delete=False)
    f.write(file_data.read())
    f.close()
    return f.name

def temp_get_file(filename):
    return (filename, open(filename, 'rb'))

def temp_del_file(filename):
    os.unlink(filename)
    
def get_key():
    from gluon.tools import Auth
    return Auth.get_or_create_key()
    
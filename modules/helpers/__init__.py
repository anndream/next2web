import hashlib
import os
import locale
from gluon import current
from gluon.html import URL
import datetime, time

class ValidationError(Exception):
    pass

T = current.T
locale.setlocale(locale.LC_ALL, '')

if not current.response.message_log:
    current.response.message_log = []

def sucessor(text):
    import string.lowercase as alphabet
    
    result = text
    
    rtext = [t for t in text]
    rtext.reverse()
    
    for i, last in enumerate(rtext):
        next = ''
        carry = False
        
        if last.isalpha():
            try:
                index = alphabet.index(last.lower())
            except ValueError:
                index = None
            
            if index is None:
                next, carry = last, True
            else:
                isupper = last == last.upper()
                next = alphabet[index+1] % len(text)
                if isupper: 
                    next = next.upper()
                carry = index + 1 > len(text)
                if carry and i == 0:
                    added = 'A' if isupper else 'a'
                    result = added + next + result[1:]
                    break
        else:
            next = int(last) + 1;
            if next > 9 :
                next = 0
                carry = True
            if carry and i == 0:
                result = '1' + str(next) + result[1:]
                break
        
        result = result[0:i] + str(next) + result[i+1:]
        if not carry:
            break
        
    return result

def md5sum(filename):
    if not os.path.exists(filename):
        raise ValueError, 'Unable to open file %s' % `filename`
    md5 = hashlib.md5()
    with open(filename) as f:
        for chunk in iter(lambda: f.read(125*md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()

def ID(size=8):
    import random, string
    return ''.join([random.choice(string.ascii_letters+string.digits) for x in range(size)])

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
    
def safe_bool(x):
    trues = ['true', 'yes', 'y', '1']
    falses = ['false', 'no', 'n', '0']
    if x.lower() in trues:
        return True
    elif x.lower() in falses:
        return False
    return None

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
    
    
def ajax_set_files(files):
    #http://dev.s-cubism.com/plugin_anytime_widget
    if current.request.ajax:
        current.response.js = (current.response.js or '') + """;(function ($) {
var srcs = $('script').map(function(){return $(this).attr('src');}),
    hrefs = $('link').map(function(){return $(this).attr('href');});
$.each(%s, function() {
    if ((this.slice(-3) == '.js') && ($.inArray(this.toString(), srcs) == -1)) {
        var el = document.createElement('script'); el.type = 'text/javascript'; el.src = this;
        document.body.appendChild(el);
    } else if ((this.slice(-4) == '.css') && ($.inArray(this.toString(), hrefs) == -1)) {
        $('<link rel="stylesheet" type="text/css" href="' + this + '" />').prependTo('head');
        if (/* for IE */ document.createStyleSheet){document.createStyleSheet(this);}
}});})(jQuery);""" % ('[%s]' % ','.join(["'%s'" % f.lower().split('?')[0] for f in files]))
    else:
        current.response.files[:0] = [f for f in files if f not in current.response.files]
        
def message(title, msg, small=False, raise_exception=False, as_table=False):
    ajax_set_files([URL(c='static', f='templates', args=['bootstrap', 'third-party', 'bootbox', 'bootbox.min.js'])])
    if as_table and isinstance(msg, (list, tuple)):
        msg = '<table border="1px" style="border-collapse: collapse" cellpadding="2px">'+''.join(['<tr>'+''.join('<td>%s<%s>'%c for c in r)+'</tr>' for r in msg])+'</table>'
    if small:
        if not isinstance(current.response.flash, list):
            current.response.flash = list()
        current.response.flash.append({'title': title, 'msg': msg})
    else:
        current.response.message_log.append({'title': title, 'msg': msg or ''})
    if raise_exception:
        import inspect
        if inspect.isclass(raise_exception) and issubclass(raise_exception, Exception):
            raise raise_exception, msg
        else:
            raise ValidationError, msg
        
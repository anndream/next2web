
from gluon import current

from helpers import temp_store_file, temp_get_file, temp_del_file

class BaseStorage(object):
    KEY = 'storage'
    DATA_KEY = 'storage_data'
    FILE_KEY = 'storage_file'
    EXTRA_KEY = 'storage_extra'
     
    def __init__(self, prefix):        
        self.prefix = 'stored_%s' % prefix
        self.request = current.request
        
    def init_data(self):
        self.data = {
            self.KEY : None,
            self.DATA_KEY: {},            
            self.FILE_KEY: {},
            self.DATA_KEY: {}
        }
        
    def reset(self):
        self.init_data()
        
    def _get_current(self):
        return self.data[self.STEP_KEY]
    
    def _set_current(self, step):
        self.data[self.STEP_KEY] = step
        
    current = property(_get_current, _set_current)
    
    def _get_extra_data(self):
        return self.data[self.EXTRA_DATA_KEY]
    
    def _set_extra_data(self, extra_data ):
        self.data[self.EXTRA_DATA_KEY] = extra_data
    
    extra_data = property(_get_extra_data, _set_extra_data)
    
    def get_data(self, step):
        return self.data[self.KEY][step]
    
    def set_data(self, step, cleaned_data):
        self.data[self.KEY][step] = cleaned_data
        
    @property
    def current_data(self):
        return self.get_data(self.current)
    
    def get_files(self, step):
        stored_files = self.data[self.KEY].get(step, {})
        
        files = {}
        for field, field_dict in stored_files.iteritems():
            field_dict = dict((unicode(k),v) for k, v in field_dict.iteritems())
            tmp_name = field_dict.pop('tmp_name')
            files[field] = temp_get_file(tmp_name)
            files[field].filename = field_dict.pop('filename') 
            
        return files
    
    def set_files(self, step, files):
        from gluon.contenttype import contenttype
        if step not in self.data[self.FILE_KEY]:
            self.data[self.FILE_KEY][step] = {}
        
        for field, field_file in (files or {}).iteritems():
            tmp_file = temp_store_file(field_file)
            file_dict = {
                'tmp_name' : tmp_file,
                'filename': field_file.filename,
                'content-type': contenttype(field_file.filename)
            }
            self.data[self.KEY][step][field] = file_dict
            
    @property
    def current_files(self):
        return self.get_files(self.current)
    
    def update_response(self, response):
        pass
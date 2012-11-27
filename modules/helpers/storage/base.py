
from gluon import current
from helpers import temp_store_file, temp_get_file, temp_del_file

class BaseStorage(object):
    KEY = 'storage'
    DATA_KEY = 'storage_data'
    FILE_KEY = 'storage_file'
     
    def __init__(self, prefix):        
        self.prefix = 'stored_%s' % prefix
        self.request = current.request
        
    def init_data(self):
        self.data = {
            self.KEY : None,
            self.DATA_KEY: {},            
            self.FILE_KEY: {},
        }
        
    def reset(self):
        self.init_data()
        
    def _get_current(self):
        return self.data[self.KEY]
    
    def _set_current(self, step):
        self.data[self.KEY] = step
        
    current = property(_get_current, _set_current)
    
    def get_data(self, step):
        if not self.data[self.DATA_KEY].has_key(step):
            self.data[self.DATA_KEY][step] = []
        return self.data[self.DATA_KEY][step]
    
    def set_data(self, step, cleaned_data):
        if step!=self.current:
            self.current = step
        if not self.data[self.DATA_KEY].has_key(step):
            self.data[self.DATA_KEY][step] = []
        self.data[self.DATA_KEY][step] = cleaned_data
        
    data = property(get_data, set_data)
        
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
        
        for field, (filename, data)  in (files or {}).iteritems():
            tmp_file = temp_store_file(data)
            file_dict = {
                'tmp_name' : tmp_file,
                'filename': filename,
                'content-type': contenttype(filename)
            }
            self.data[self.KEY][step][field] = file_dict
            
    @property
    def current_files(self):
        return self.get_files(self.current)
    
    def update_response(self, response):
        pass
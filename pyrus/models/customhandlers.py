import jsonpickle
from datetime import datetime
from datetime import time
from . import constants

class FormFieldHandler(jsonpickle.handlers.BaseHandler):
    
    def flatten(self, obj, data):
        if obj.id:
            data['id'] = obj.id
        if obj.name:
            data['name'] = obj.name

        #ignore readonly fields
        if obj.type in ['step', 'status', 'note', 'author', 'project', 'creation_date']:
            return data

        if obj.value is not None:
            data['value'] = self._get_flatten_value(obj.type, obj.value)
        return data
    
    def _get_flatten_value(self, type, value):
        if isinstance(value, str):
            return value

        if type == 'due_date_time':
            return value.strftime(constants.DATE_TIME_FORMAT)
        if type in ['date', 'due_date']:
            return value.strftime(constants.DATE_FORMAT)
        if type == 'time':
            if isinstance(value, time):
                return time.strftime(value, constants.TIME_FORMAT)
            return datetime.strftime(value, constants.TIME_FORMAT)
        if type == 'file':
            if not isinstance(value, list):
                return
                
        p = jsonpickle.Pickler(unpicklable=False)
        return p.flatten(value)


class ChannelHandler(jsonpickle.handlers.BaseHandler):
    
    def flatten(self, obj, data):
        if obj.type:
            data['type'] = obj.type
        return data
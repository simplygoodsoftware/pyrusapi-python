# pylint: disable=C0103
# pylint: disable=R0903
# pylint: disable=too-many-instance-attributes

from . import entities

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

class BaseResponse(object):
    error_code = None
    error = None

    def __init__(self, **kwargs):
        if 'error_code' in kwargs:
            self.error_code = kwargs['error_code']
        if 'error' in kwargs:
            self.error = kwargs['error']
        
class AuthResponse(BaseResponse):
    access_token = None

    def __init__(self, **kwargs):
        if 'access_token' in kwargs:
            self.access_token = kwargs['access_token']
            self.success = True
        else:
            self.success = False
        super(AuthResponse, self).__init__(**kwargs)

class FormResponse(BaseResponse):
    id = None
    name = None
    steps = None
    fields = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'steps' in kwargs:
            self.steps = kwargs['steps']
        if 'fields' in kwargs:
            self.fields = []
            for field in kwargs['fields']:
                self.fields.append(entities.FormField(**field))
        super(FormResponse, self).__init__(**kwargs)

class FormsResponse(BaseResponse):
    forms = None

    def __init__(self, **kwargs):
        if 'forms' in kwargs:
            self.forms = []
            for form in kwargs['forms']:
                self.forms.append(FormResponse(**form))
        super(FormsResponse, self).__init__(**kwargs)

class TaskResponse(BaseResponse):
    task = None
    def __init__(self, **kwargs):
        if 'task' in kwargs:
            self.task = entities.TaskWithComments(**kwargs['task'])
        super(TaskResponse, self).__init__(**kwargs)

class ContactsResponse(BaseResponse):
    organizations = None

    def __init__(self, **kwargs):
        if 'organizations' in kwargs:
            self.organizations = []
            for organization in kwargs['organizations']:
                self.organizations.append(entities.Organization(**organization))
        super(ContactsResponse, self).__init__(**kwargs)

class CatalogResponse(BaseResponse):
    items = None
    catalog_id = None
    catalog_headers = None

    def __init__(self, **kwargs):
        if 'catalog_id' in kwargs:
            self.catalog_id = kwargs['catalog_id']
        if 'items' in kwargs:
            self.items = []
            for item in kwargs['items']:
                self.items.append(entities.CatalogItem(**item))
        if 'catalog_headers' in kwargs:
            self.catalog_headers = []
            for item in kwargs['catalog_headers']:
                self.catalog_headers.append(entities.CatalogHeader(**item))
        super(CatalogResponse, self).__init__(**kwargs)

class FormRegisterResponse(BaseResponse):
    tasks = None
    def __init__(self, **kwargs):
        if 'tasks' in kwargs:
            self.tasks = []
            for task in kwargs['tasks']:
                self.tasks.append(entities.Task(**task))
        super(FormRegisterResponse, self).__init__(**kwargs)

class UploadResponse(BaseResponse):
    guid = None
    md5_hash = None
    def __init__(self, **kwargs):
        if 'guid' in kwargs:
            self.guid = kwargs['guid']
        if 'md5_hash' in kwargs:
            self.md5_hash = kwargs['md5_hash']
        super(UploadResponse, self).__init__(**kwargs)

class ListsResponse(BaseResponse):
    lists = None
    def __init__(self, **kwargs):
        if 'lists' in kwargs:
            self.lists = []
            for lst in kwargs['lists']:
                self.lists.append(entities.TaskList(**lst))
        super(ListsResponse, self).__init__(**kwargs)

class TaskListResponse(BaseResponse):
    tasks = None
    has_more = None
    def __init__(self, **kwargs):
        if 'has_more' in kwargs:
            self.has_more = kwargs['has_more']
        if 'tasks' in kwargs:
            self.tasks = []
            for task in kwargs['tasks']:
                self.tasks.append(entities.TaskHeader(**task))
        super(TaskListResponse, self).__init__(**kwargs)

class DownloadResponse(BaseResponse):
    filename = None
    raw_file = None
    def __init__(self, filename, raw_file):
        self.filename = filename
        self.raw_file = raw_file
        super(DownloadResponse, self).__init__(**{})

class SyncCatalogResponse(BaseResponse):
    apply = None
    added = None
    deleted = None
    updated = None
    catalog_headers = None
    def __init__(self, **kwargs):
        if 'apply' in kwargs:
            self.apply = kwargs['apply']
        if 'added' in kwargs:
            self.added = []
            for added_item in kwargs['added']:
                self.added.append(entities.CatalogItem(**added_item))
        if 'updated' in kwargs:
            self.updated = []
            for updated_item in kwargs['updated']:
                self.updated.append(entities.CatalogItem(**updated_item))
        if 'deleted' in kwargs:
            self.deleted = []
            for deleted_item in kwargs['deleted']:
                self.deleted.append(entities.CatalogItem(**deleted_item))
        if 'catalog_headers' in kwargs:
            self.catalog_headers = []
            for header in kwargs['catalog_headers']:
                self.catalog_headers.append(entities.CatalogHeader(**header))
        super(SyncCatalogResponse, self).__init__(**kwargs)
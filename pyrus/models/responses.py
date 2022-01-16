# pylint: disable=C0103
# pylint: disable=R0903
# pylint: disable=too-many-instance-attributes

from . import entities
from . import constants


class BaseResponse(object):
    """
        error_code (:obj:`str`): Error code
        error (:obj:`str`): Human readable string describing the error
    """

    error_code = None
    error = None
    original_response = None

    def __init__(self, **kwargs):
        self.original_response = kwargs
        if 'error_code' in kwargs:
            self.error_code = kwargs['error_code']
        if 'error' in kwargs:
            self.error = kwargs['error']


class AuthResponse(BaseResponse):
    """
        AuthResponse
        
        Attributes:
            access_token (:obj:`str`): User's access token
            success (:obj:`bool`): True if the user was successfully authenticated. False otherwise.
    """
    __doc__ += BaseResponse.__doc__

    access_token = None

    def __init__(self, **kwargs):
        if 'access_token' in kwargs:
            self.access_token = kwargs['access_token']
            self.success = True
        else:
            self.success = False
        super(AuthResponse, self).__init__(**kwargs)


class FormResponse(BaseResponse):
    """
        FormResponse
        
        Attributes:
            id (:obj:`int`): Form id
            name (:obj:`str`): Form name
            steps (:obj:`dict`): Form steps
                key (:obj:`int`): Step number
                value (:obj:`str`): Step name
            fields (:obj:`list` of :obj:`models.entities.FormField`): List of form fields
            deletedOrClosed (:obj:`bool`): Form state
            folder (:obj:`list` of :obj:`str`): Folder of form
    """
    __doc__ += BaseResponse.__doc__

    id = None
    name = None
    steps = None
    fields = None
    deletedOrClosed = None
    folder = None

    @property
    def flat_fields(self):
        return self._get_flat_fields(self.fields)

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
        if 'deleted_or_closed' in kwargs:
            self.deletedOrClosed = kwargs['deleted_or_closed']
        if 'folder' in kwargs:
            self.folder = []
            for fld in kwargs['folder']:
                self.folder.append(fld)
        super(FormResponse, self).__init__(**kwargs)

    def _get_flat_fields(self, fields):
        res = []
        if not fields:
            return res
        for field in fields:
            res.append(field)
            if not field.info:
                continue
            if field.info.fields:
                res.extend(self._get_flat_fields(field.info.fields))
            elif field.info.options:
                for option in field.info.options:
                    res.extend(self._get_flat_fields(option.fields))
            elif field.info.columns:
                res.extend(field.info.columns)

        return res


class FormsResponse(BaseResponse):
    """
        FormsResponse
        
        Attributes:
            forms (:obj:`list` of :obj:`models.responses.FormResponse`): List of form templates
    """
    __doc__ += BaseResponse.__doc__

    forms = None

    def __init__(self, **kwargs):
        if 'forms' in kwargs:
            self.forms = []
            for form in kwargs['forms']:
                self.forms.append(FormResponse(**form))
        super(FormsResponse, self).__init__(**kwargs)


class TaskResponse(BaseResponse):
    """
        TaskResponse
        
        Attributes:
            task (:obj:`models.entities.TaskWithComments`): Task
    """
    __doc__ += BaseResponse.__doc__

    task = None

    def __init__(self, **kwargs):
        if 'task' in kwargs:
            self.task = entities.TaskWithComments(**kwargs['task'])
        super(TaskResponse, self).__init__(**kwargs)


class ContactsResponse(BaseResponse):
    """
        ContactsResponse
        
        Attributes:
            organizations (:obj:`list` of :obj:`models.entities.Organization`): List of available contacts in each organization
    """
    __doc__ += BaseResponse.__doc__

    organizations = None

    def __init__(self, **kwargs):
        if 'organizations' in kwargs:
            self.organizations = []
            for organization in kwargs['organizations']:
                self.organizations.append(entities.Organization(**organization))
        super(ContactsResponse, self).__init__(**kwargs)


class CatalogResponse(BaseResponse):
    """
        CatalogResponse
        
        Attributes:
            items (:obj:`list` of :obj:`models.entities.CatalogItem`): List of catalog items
            catalog_id (:obj:`int`): Catalog id
            catalog_headers (:obj:`list` of :obj:`models.entities.CatalogHeader`): List of catalog headers
    """
    __doc__ += BaseResponse.__doc__

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
    """
        FormRegisterResponse
        
        Attributes:
            tasks (:obj:`list` of :obj:`models.entities.Task`): List of tasks based on the form template
            csv (:obj:`str`): csv response (if csv format was requested)
    """
    __doc__ += BaseResponse.__doc__

    tasks = None
    csv = None

    def __init__(self, **kwargs):
        if 'tasks' in kwargs:
            self.tasks = []
            for task in kwargs['tasks']:
                self.tasks.append(entities.Task(**task))
        super(FormRegisterResponse, self).__init__(**kwargs)


class UploadResponse(BaseResponse):
    """
        UploadResponse
        
        Attributes:
            guid (:obj:`str`): Unique identifier of the downloaded file
            md5_hash (:obj:`str`): File hash calculated by the MD5 algorithm
    """
    __doc__ += BaseResponse.__doc__

    guid = None
    md5_hash = None

    def __init__(self, **kwargs):
        if 'guid' in kwargs:
            self.guid = kwargs['guid']
        if 'md5_hash' in kwargs:
            self.md5_hash = kwargs['md5_hash']
        super(UploadResponse, self).__init__(**kwargs)


class ListsResponse(BaseResponse):
    """
        ListsResponse
        
        Attributes:
            lists (:obj:`list` of :obj:`models.entities.TaskList`): All the lists available to the users
    """
    __doc__ += BaseResponse.__doc__

    lists = None

    def __init__(self, **kwargs):
        if 'lists' in kwargs:
            self.lists = []
            for lst in kwargs['lists']:
                self.lists.append(entities.TaskList(**lst))
        super(ListsResponse, self).__init__(**kwargs)


class TaskListResponse(BaseResponse):
    """
        TaskListResponse
        
        Attributes:
            tasks (:obj:`list` of :obj:`models.entities.TaskHeader`): List of the task in the specified list
            has_more (:obj:`bool`): True if not all tasks from the list were returned. False otherwise
    """
    __doc__ += BaseResponse.__doc__

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
    """
        DownloadResponse
        
        Attributes:
            filename (:obj:`str`): Filename
            raw_file (:obj:`bytes`): Raw file
    """
    __doc__ += BaseResponse.__doc__

    filename = None
    raw_file = None

    def __init__(self, filename, raw_file):
        self.filename = filename
        self.raw_file = raw_file
        super(DownloadResponse, self).__init__(**{})


class SyncCatalogResponse(BaseResponse):
    """
        SyncCatalogResponse
        
        Attributes:
            apply (:obj:`bool`): Indicates if changes were applied
            added (:obj:`list` of obj`models.entities.CatalogItem`): Added catalog items
            deleted (:obj:`list` of obj`models.entities.CatalogItem`): Deleted catalog items
            updated (:obj:`list` of obj`models.entities.CatalogItem`): Updated catalog items
            catalog_headers (:obj:`list` of obj`models.entities.CatalogHeader`): List of catalog headers
    """
    __doc__ += BaseResponse.__doc__

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

class ProfileResponse(BaseResponse):
    """
        ProfileResponse
        
        Attributes:
            person_id (:obj:`int`): Person id
            first_name (:obj:`str`): Person first name
            last_name (:obj:`str`): Person last name
            email(:obj:`str`): Person email
            locale(:obj:`str`): Person locale (ru-RU/en-US/en-GB)
            organization_id(:obj:`int`) Person organization id
            organization(:obj:`obj`models.entities.Organization) Person organization
    """
    __doc__ += BaseResponse.__doc__

    person_id = None
    first_name = None
    last_name = None
    email = None
    locale = None
    organization_id = None
    organization = None

    def __init__(self, **kwargs):
        if 'person_id' in kwargs:
            self.person_id = kwargs['person_id']
        if 'first_name' in kwargs:
            self.first_name = kwargs['first_name']
        if 'last_name' in kwargs:
            self.last_name = kwargs['last_name']
        if 'email' in kwargs:
            self.email = kwargs['email']
        if 'locale' in kwargs:
            self.locale = kwargs['locale']
        if 'organization_id' in kwargs:
            self.organization_id = kwargs['organization_id']
        if 'organization' in kwargs:
            self.organization = entities.Organization(**kwargs['organization'])
        super(ProfileResponse, self).__init__(**kwargs)


class CalendarResponse(BaseResponse):
    """
            CalendarResponse

            Attributes:
                tasks (:obj:`list` of :obj:`models.entities.TaskWithComments`): List of the task with only last comment in the specified list
                has_more (:obj:`bool`): True if not all tasks from the list were returned. False otherwise
        """
    __doc__ += BaseResponse.__doc__

    tasks = None
    has_more = None

    def __init__(self, **kwargs):
        if 'has_more' in kwargs:
            self.has_more = kwargs['has_more']
        if 'tasks' in kwargs:
            self.tasks = []
            for task in kwargs['tasks']:
                self.tasks.append(entities.TaskWithComments(**task))
        super(CalendarResponse, self).__init__(**kwargs)

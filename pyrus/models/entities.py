# pylint: disable=C0103
# pylint: disable=R0903
# pylint: disable=too-many-instance-attributes

from datetime import datetime

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DATE_FORMAT = '%Y-%m-%d'

class FormField(object):
    id = None
    type = None
    name = None
    info = None
    value = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'type' in kwargs:
            self.type = kwargs['type']
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'info' in kwargs:
            self.info = FormFieldInfo(**kwargs['info'])
        if 'value' in kwargs:
            if self.type:
                self.value = _create_field_value(self.type, kwargs['value'])
            else:
                self.value = kwargs['value']

class FormFieldInfo(object):
    required_step = None
    immutable_step = None
    options = None
    catalog_id = None
    columns = None
    fields = None

    def __init__(self, **kwargs):
        if 'required_step' in kwargs:
            self.required_step = kwargs['required_step']
        if 'immutable_step' in kwargs:
            self.immutable_step = kwargs['immutable_step']
        if 'options' in kwargs:
            self.options = []
            for option in kwargs['options']:
                self.options.append(ChoiceOption(**option))
        if 'catalog_id' in kwargs:
            self.catalog_id = kwargs['catalog_id']
        if 'columns' in kwargs:
            self.columns = []
            for column in kwargs['columns']:
                self.columns.append(FormField(**column))
        if 'fields' in kwargs:
            self.fields = []
            for field in kwargs['fields']:
                self.fields.append(FormField(**field))

class ChoiceOption(object):
    choice_id = None
    choice_value = None
    fields = None

    def __init__(self, **kwargs):
        if 'choice_id' in kwargs:
            self.choice_id = kwargs['choice_id']
        if 'choice_value' in kwargs:
            self.choice_value = kwargs['choice_value']
        if 'fields' in kwargs:
            self.fields = []
            for field in kwargs['fields']:
                self.fields.append(FormField(**field))

class TaskHeader(object):
    id = None
    text = None
    create_date = None
    last_modified_date = None
    author = None
    close_date = None
    responsible = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'text' in kwargs:
            self.text = kwargs['text']
        if 'create_date' in kwargs:
            self.create_date = datetime.strptime(kwargs['create_date'], DATE_TIME_FORMAT)
        if 'last_modified_date' in kwargs:
            self.last_modified_date = datetime.strptime(kwargs['last_modified_date'], DATE_TIME_FORMAT)
        if 'author' in kwargs:
            self.author = Person(**kwargs['author'])
        if 'close_date' in kwargs:
            self.close_date = datetime.strptime(kwargs['close_date'], DATE_TIME_FORMAT)
        if 'responsible' in kwargs:
            self.responsible = Person(**kwargs['responsible'])

class Task(TaskHeader):
    due_date = None
    due = None
    duration = None
    form_id = None
    attachments = None
    fields = None
    approvals = None
    participants = None
    scheduled_date = None
    list_ids = None

    def __init__(self, **kwargs):
        if 'due_date' in kwargs:
            self.due_date = datetime.strptime(kwargs['due_date'], DATE_FORMAT)
        if 'due' in kwargs:
            self.due = datetime.strptime(kwargs['due'], DATE_TIME_FORMAT)
        if 'duration' in kwargs:
            self.duration = kwargs['duration']
        if 'scheduled_date' in kwargs:
            self.scheduled_date = datetime.strptime(kwargs['scheduled_date'], DATE_FORMAT)
        if 'form_id' in kwargs:
            self.form_id = kwargs['form_id']
        if 'attachments' in kwargs:
            self.attachments = []
            for attachment in kwargs['attachments']:
                self.attachments.append(File(**attachment))
        if 'fields' in kwargs:
            self.fields = []
            for field in kwargs['fields']:
                self.fields.append(FormField(**field))
        if 'approvals' in kwargs:
            self.approvals = []
            for idx, approval in enumerate(kwargs['approvals']):
                self.approvals.append([])
                for curr_step in approval:
                    self.approvals[idx].append(Approval(**curr_step))
        if 'participants' in kwargs:
            self.participants = []
            for participant in kwargs['participants']:
                self.participants.append(Person(**participant))
        if 'list_ids' in kwargs:
            self.list_ids = []
            for lst in kwargs['list_ids']:
                self.list_ids.append(lst)
        super(Task, self).__init__(**kwargs)

class TaskWithComments(Task):
    comments = None

    def __init__(self, **kwargs):
        if 'comments' in kwargs:
            self.comments = []
            for comment in kwargs['comments']:
                self.comments.append(TaskComment(**comment))
        super(TaskWithComments, self).__init__(**kwargs)

class Person(object):
    id = None
    first_name = None
    last_name = None
    email = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'first_name' in kwargs:
            self.first_name = kwargs['first_name']
        if 'last_name' in kwargs:
            self.last_name = kwargs['last_name']
        if 'email' in kwargs:
            self.email = kwargs['email']

class File(object):
    id = None
    name = None
    size = None
    md5 = None
    url = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'size' in kwargs:
            self.size = kwargs['size']
        if 'md5' in kwargs:
            self.md5 = kwargs['md5']
        if 'url' in kwargs:
            self.url = kwargs['url']

class Approval(object):
    person = None
    approval_choice = None
    step = None

    def __init__(self, **kwargs):
        if 'person' in kwargs:
            self.person = Person(**kwargs['person'])
        if 'approval_choice' in kwargs:
            self.approval_choice = kwargs['approval_choice']
        if 'step' in kwargs:
            self.step = kwargs['step']

class TaskComment(object):
    id = None
    text = None
    create_date = None
    author = None
    reassigned_to = None
    field_updates = None
    approval_choice = None
    reset_to_step = None
    approvals_added = None
    approvals_removed = None
    participants_added = None
    participants_added = None
    participants_removed = None
    due_date = None
    due = None
    duration = None
    attachments = None
    action = None
    scheduled_date = None
    cancel_schedule = None
    added_list_ids = None
    removed_list_ids = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'text' in kwargs:
            self.text = kwargs['text']
        if 'create_date' in kwargs:
            self.create_date = datetime.strptime(kwargs['create_date'], DATE_TIME_FORMAT)
        if 'author' in kwargs:
            self.author = Person(**kwargs['author'])
        if 'reassigned_to' in kwargs:
            self.reassigned_to = Person(**kwargs['reassigned_to'])
        if 'field_updates' in kwargs:
            self.field_updates = []
            for field in kwargs['field_updates']:
                self.field_updates.append(FormField(**field))
        if 'approval_choice' in kwargs:
            self.approval_choice = kwargs['approval_choice']
        if 'reset_to_step' in kwargs:
            self.reset_to_step = kwargs['reset_to_step']
        if 'approvals_added' in kwargs:
            self.approvals_added = []
            for idx, approval in enumerate(kwargs['approvals_added']):
                self.approvals_added.append([])
                for curr_step in approval:
                    self.approvals_added[idx].append(Approval(**curr_step))
        if 'approvals_removed' in kwargs:
            self.approvals_removed = []
            for idx, approval in enumerate(kwargs['approvals_removed']):
                self.approvals_removed.append([])
                for curr_step in approval:
                    self.approvals_removed[idx].append(Approval(**curr_step))
        if 'participants_added' in kwargs:
            self.participants_added = []
            for participant in kwargs['participants_added']:
                self.participants_added.append(Person(**participant))
        if 'participants_removed' in kwargs:
            self.participants_removed = []
            for participant in kwargs['participants_removed']:
                self.participants_removed.append(Person(**participant))
        if 'due_date' in kwargs:
            self.due_date = datetime.strptime(kwargs['due_date'], DATE_FORMAT)
        if 'due' in kwargs:
            self.due = datetime.strptime(kwargs['due'], DATE_TIME_FORMAT)
        if 'duration' in kwargs:
            self.duration = kwargs['duration']
        if 'attachments' in kwargs:
            self.attachments = []
            for attachment in kwargs['attachments']:
                self.attachments.append(File(**attachment))
        if 'action' in kwargs:
            self.action = kwargs['action']
        if 'scheduled_date' in kwargs:
            self.scheduled_date = datetime.strptime(kwargs['scheduled_date'], DATE_FORMAT)
        if 'cancel_schedule' in kwargs:
            self.cancel_schedule = kwargs['cancel_schedule']
        if 'added_list_ids' in kwargs:
            self.added_list_ids = []
            for lst in kwargs['added_list_ids']:
                self.added_list_ids.append(lst)
        if 'removed_list_ids' in kwargs:
            self.removed_list_ids = []
            for lst in kwargs['removed_list_ids']:
                self.removed_list_ids.append(lst)

class Organization(object):
    id = None
    name = None
    persons = None
    roles = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'persons' in kwargs:
            self.persons = []
            for person in kwargs['persons']:
                self.persons.append(Person(**person))
        if 'roles' in kwargs:
            self.roles = []
            for role in kwargs['roles']:
                self.roles.append(Role(**role))

class Role(object):
    id = None
    name = None
    member_ids = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'member_ids' in kwargs:
            self.member_ids = []
            for member_id in kwargs['member_ids']:
                self.member_ids.append(member_id)

class CatalogItem(object):
    item_id = None
    values = None
    headers = None

    def __init__(self, **kwargs):
        if 'headers' in kwargs:
            self.headers = kwargs['headers']
        if 'item_id' in kwargs:
            self.item_id = kwargs['item_id']
        if 'values' in kwargs:
            self.values = []
            for value in kwargs['values']:
                self.values.append(value)

class Table(list):
    def __init__(self, *args):
        list.__init__(self)
        for value in args:
            self.append(TableRow(**value))

class TableRow(object):
    row_id = None
    cells = None
    def __init__(self, **kwargs):
        if 'row_id' in kwargs:
            self.row_id = kwargs['row_id']
        if 'cells' in kwargs:
            self.cells = []
            for cell in kwargs['cells']:
                if isinstance(cell, FormField):
                    self.cells.append(cell)
                else:
                    self.cells.append(FormField(**cell))

class Title(object):
    checkmark = None
    fields = None

    def __init__(self, **kwargs):
        if 'checkmark' in kwargs:
            self.checkmark = kwargs['checkmark']
        if 'fields' in kwargs:
            self.fields = []
            for field in kwargs['fields']:
                self.fields.append(FormField(**field))

class Checkmark(object):
    choice_id = None
    fields = None

    def __init__(self, **kwargs):
        if 'choice_id' in kwargs:
            self.choice_id = kwargs['choice_id']
        if 'fields' in kwargs:
            self.fields = []
            for field in kwargs['fields']:
                self.fields.append(FormField(**field))

class Projects(object):
    projects = None

    def __init__(self, **kwargs):
        if 'projects' in kwargs:
            self.projects = []
            for project in kwargs['projects']:
                self.projects.append(Project(**project))

class FormLink(object):
    task_id = None
    subject = None

    def __init__(self, **kwargs):
        if 'task_id' in kwargs:
            self.task_id = kwargs['task_id']
        if 'subject' in kwargs:
            self.subject = kwargs['subject']

class Project(object):
    id = None
    name = None
    parent = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'parent' in kwargs:
            self.parent = Project(**kwargs['parent'])

class FormRegisterFilter(object):
    def __init__(self, **kwargs):
        self.field_id = kwargs['field_id']
        self.operator = kwargs['operator']
        self.values = kwargs['values']

class EqualsFilter(FormRegisterFilter):
    def __init__(self, field_id, value):
        _validate_field_id(field_id)
        super(EqualsFilter, self).\
            __init__(field_id=field_id, operator='equals', values=_get_value(value))

class GreaterThanFilter(FormRegisterFilter):
    def __init__(self, field_id, value):
        _validate_field_id(field_id)
        super(GreaterThanFilter, self).\
            __init__(field_id=field_id, operator='greater_than', values=_get_value(value))

class LessThanFilter(FormRegisterFilter):
    def __init__(self, field_id, value):
        _validate_field_id(field_id)
        super(LessThanFilter, self).\
            __init__(field_id=field_id, operator='less_than', values=_get_value(value))

class RangeFilter(FormRegisterFilter):
    def __init__(self, field_id, values):
        _validate_field_id(field_id)
        if not isinstance(values, list):
            raise TypeError('values must be a list.')
        if len(values) != 2:
            raise TypeError('values length must be equal 2.')
        formated_values = []
        for value in values:
            formated_values.append(_get_value(value))
        super(RangeFilter, self).\
            __init__(field_id=field_id, operator='range', values=formated_values)

class IsInFilter(FormRegisterFilter):
    def __init__(self, field_id, values):
        _validate_field_id(field_id)
        if not isinstance(values, list):
            raise TypeError('values must be a list.')
        formated_values = []
        for value in values:
            formated_values.append(_get_value(value))
        super(IsInFilter, self).\
            __init__(field_id=field_id, operator='is_in', values=formated_values)

class TaskList(object):
    id = None
    name = None
    children = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'children' in kwargs:
            self.children = []
            for child in kwargs['children']:
                self.children.append(TaskList(**child))

def _get_value(value):
    if isinstance(value, datetime):
        return value.strftime(DATE_FORMAT)
    return value

def _validate_field_id(field_id):
    if not isinstance(field_id, int):
        raise TypeError('field_id must be valid int.')

def _create_field_value(field_type, value):
    if field_type in ['text', 'money', 'number', 'time', 'checkmark', 'email',
                      'phone', 'flag', 'step', 'status', 'note']:
        return value
    if field_type in ['date', 'create_date', 'due_date']:
        return datetime.strptime(value, DATE_FORMAT)
    if field_type == 'due_date_time':
        return datetime.strptime(value, DATE_TIME_FORMAT)
    if field_type == 'catalog':
        return CatalogItem(**value)
    if field_type == 'file':
        res = []
        for file in value:
            res.append(File(**file))
        return res
    if field_type in ['person', 'author']:
        return Person(**value)
    if field_type == 'table':
        return Table(*value)
    if field_type == 'title':
        return Title(**value)
    if field_type == 'checkmark':
        return Checkmark(**value)
    if field_type == 'project':
        return Projects(**value)
    if field_type == 'form_link':
        return FormLink(**value)

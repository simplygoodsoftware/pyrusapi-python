# pylint: disable=C0103
# pylint: disable=R0903
# pylint: disable=too-many-instance-attributes

from datetime import datetime
from datetime import timezone

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = "%H:%M"

class FormField(object):
    """
        Form field
        
        Attributes:
            id (:obj:`int`): Field id
            type (:obj:`str`): Field type
            name (:obj:`str`): Field name
            info (:obj:`models.entitites.FormFieldInfo`): Additional field information
            value (:obj:`object`, optional): Field value
            parent_id (:obj:`int`, optional) Parent field id (returned if field has parent)
            row_id (:obj:`int`, optional) Table row id (returned if field is in table)
    """

    id = None
    type = None
    name = None
    info = None
    value = None
    parent_id = None
    row_id = None

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
        if 'parent_id' in kwargs:
            self.parent_id = kwargs['parent_id']
        if 'row_id' in kwargs:
            self.row_id = kwargs['row_id']

class FormFieldInfo(object):
    """
        Additional form field information
        
        Attributes:
            required_step (:obj:`int`): Indicates the step number where the field becomes required for filling
            immutable_step (:obj:`int`): indicates the step number from which the user can't change the field value
            options (:obj:`list` of :obj:`models.entitites.ChoiceOption`): Choice options for multiple_choice field
            catalog_id (:obj:`int`): Catalog id for catalog field
            columns (:obj:`list` of :obj:`models.entitites.FormField`): Columns description for table field
            fields (:obj:`list` of :obj:`models.entitites.FormField`): Child fields description for title field
    """

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
    """
        multiple_choice options description
        
        Attributes:
            choice_id (:obj:`int`): Choice id
            choice_value (:obj:`str`): Choice name
            fields (:obj:`list` of :obj:`models.entitites.FormField`): Child fields for the specified choice_id
            deleted (:obj:`bool`): Is choice deleted
    """
    choice_id = None
    choice_value = None
    fields = None
    deleted = None

    def __init__(self, **kwargs):
        if 'choice_id' in kwargs:
            self.choice_id = kwargs['choice_id']
        if 'choice_value' in kwargs:
            self.choice_value = kwargs['choice_value']
        if 'fields' in kwargs:
            self.fields = []
            for field in kwargs['fields']:
                self.fields.append(FormField(**field))
        if 'deleted' in kwargs:
            self.deleted = kwargs['deleted']

class TaskHeader(object):
    """
        Task header
        
        Attributes:
            id (:obj:`int`): Task id
            create_date (:obj:`datetime`): Task creation date
            last_modified_date (:obj:`datetime`): Task last modified date
            close_date (:obj:`datetime`): Task closing date
            author (:obj:`models.entities.Person`): Task author
        Attributes(Simple Task):
            text (:obj:`str`): Task text
            responsible (:obj:`models.entities.Person`): Task responsible
    """

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
            self.create_date = _set_utc_timezone(datetime.strptime(kwargs['create_date'], DATE_TIME_FORMAT))
        if 'last_modified_date' in kwargs:
            self.last_modified_date = _set_utc_timezone(datetime.strptime(kwargs['last_modified_date'], DATE_TIME_FORMAT))
        if 'author' in kwargs:
            self.author = Person(**kwargs['author'])
        if 'close_date' in kwargs:
            self.close_date = _set_utc_timezone(datetime.strptime(kwargs['close_date'], DATE_TIME_FORMAT))
        if 'responsible' in kwargs:
            self.responsible = Person(**kwargs['responsible'])

class Task(TaskHeader):
    """
        Task header
        
        Attributes:
            id (:obj:`int`): Task id
            create_date (:obj:`datetime`): Task creation date
            last_modified_date (:obj:`datetime`): Task last modified date
            close_date (:obj:`datetime`): Task closing date
            author (:obj:`models.entities.Person`): Task author
            attachments (:obj:`list` of :obj:`models.entities.File`): List of task attachments
            list_ids (:obj:`list` of :obj:`int`): List of list identifiers
            parent_task_id (:obj:`int`): Parent task id
            linked_task_ids (:obj:`list` of :obj:`int`): List of linked task identifiers
            last_note_id (:obj:`int`): Id of the last comment
            subject (:obj:`str`): Task subject
        Attributes(Simple Task):
            text (:obj:`str`): Task text
            responsible (:obj:`models.entities.Person`): Task responsible
            due_date (:obj:`datetime`): Task due date
            due (:obj:`datetime`): Task due date with time
            duration (:obj:`int`): Task duration in minutes
            participants (:obj:`list` of :obj:`models.entities.Person`): List of task participants
            scheduled_date (:obj:`datetime`): task scheduled date
        Attributes(Form Task):
            form_id (:obj:`int`): Form template id
            fields (:obj:`list` of obj`models.entities.FormField`): List of field values
            approvals (:obj:`list` of :obj:`list` of :obj:`models.entities.Person`) List of approval steps.
    """

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
    parent_task_id = None
    linked_task_ids = None
    last_note_id = None
    subject = None
    @property
    def flat_fields(self):
        return _get_flat_fields(self.fields)
    
    def __init__(self, **kwargs):
        if 'subject' in kwargs:
            self.subject = kwargs['subject']
        if 'due_date' in kwargs:
            self.due_date = datetime.strptime(kwargs['due_date'], DATE_FORMAT)
        if 'due' in kwargs:
            self.due = _set_utc_timezone(datetime.strptime(kwargs['due'], DATE_TIME_FORMAT))
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
        if 'parent_task_id' in kwargs:
            self.parent_task_id = kwargs['parent_task_id']
        if 'linked_task_ids' in kwargs:
            self.linked_task_ids = []
            for linked_task_id in kwargs['linked_task_ids']:
                self.linked_task_ids.append(linked_task_id)
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
        if 'last_note_id' in kwargs:
            self.last_note_id = kwargs['last_note_id']
        super(Task, self).__init__(**kwargs)

class TaskWithComments(Task):
    """
        Task with comments
        
        Attributes:
            id (:obj:`int`): Task id
            create_date (:obj:`datetime`): Task creation date
            last_modified_date (:obj:`datetime`): Task last modified date
            close_date (:obj:`datetime`): Task closing date
            author (:obj:`models.entities.Person`): Task author
            attachments (:obj:`list` of :obj:`models.entities.File`): List of task attachments
            list_ids (:obj:`list` of :obj:`int`): List of list identifiers
            parent_task_id (:obj:`int`): Parent task id
            linked_task_ids (:obj:`list` of :obj:`int`): List of linked task identifiers
            last_note_id (:obj:`int`): Id of the last comment
            subject (:obj:`str`): Task subject
            comments (:obj:`list` of :obj:`models.entities.TaskComment`): List of task comments
        Attributes(Simple Task):
            text (:obj:`str`): Task text
            responsible (:obj:`models.entities.Person`): Task responsible
            due_date (:obj:`datetime`): Task due date
            due (:obj:`datetime`): Task due date with time
            duration (:obj:`int`): Task duration in minutes
            participants (:obj:`list` of :obj:`models.entities.Person`): List of task participants
            scheduled_date (:obj:`datetime`): task scheduled date
        Attributes(Form Task):
            form_id (:obj:`int`): Form template id
            fields (:obj:`list` of obj`models.entities.FormField`): List of field values
            approvals (:obj:`list` of :obj:`list` of :obj:`models.entities.Person`) List of approval steps.
    """

    comments = None

    def __init__(self, **kwargs):
        if 'comments' in kwargs:
            self.comments = []
            for comment in kwargs['comments']:
                self.comments.append(TaskComment(**comment))
        super(TaskWithComments, self).__init__(**kwargs)

class Person(object):
    """
        Person
        
        Attributes:
            id (:obj:`int`): Person id
            first_name (:obj:`str`): Person first name
            last_name (:obj:`str`): Person last name
            email (:obj:`str`): Person email
            type (:obj:`str`): Person type (user/bot/role)
    """

    id = None
    first_name = None
    last_name = None
    email = None
    type = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'first_name' in kwargs:
            self.first_name = kwargs['first_name']
        if 'last_name' in kwargs:
            self.last_name = kwargs['last_name']
        if 'email' in kwargs:
            self.email = kwargs['email']
        if 'type' in kwargs:
            self.type = kwargs['type']

class File(object):
    """
        File
        
        Attributes:
            id (:obj:`int`): File id
            name (:obj:`str`): File name
            size (:obj:`int`): File size in bytes
            md5 (:obj:`str`): File md5 hash
            md5 (:obj:`str`): File md5 hash
            url (:obj:`str`): Url to download the file
            size (:obj:`int`): File version
    """

    id = None
    name = None
    size = None
    md5 = None
    url = None
    version = None

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
        if 'version' in kwargs:
            self.version = kwargs['version']

class Approval(object):
    """
        Approval
        
        Attributes:
            person (:obj:`entities.models.Person`): Approval person
            approval_choice (:obj:`str`): Approval choice (approved/rejected/revoked/acknowledged)
            step (:obj:`int`): Approval step number
    """

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
    """
        Task comment
        
        Attributes:
            id (:obj:`int`): Comment id
            text (:obj:`str`): Comment text
            create_date (:obj:`datetime`): Comment creation date
            author (:obj:`models.entities.Person`): Comment author
            attachments (:obj:`list` of :obj:`models.entities.File`): List of comment attachments
            action (:obj:`str`): Activity action (finished/reopened)
            added_list_ids (:obj:`list` of :obj:`int`): List of list identifiers to which the task was added
            removed_list_ids (:obj:`list` of :obj:`int`): List of list identifiers from the task was removed
            comment_as_roles (:obj:`list` of :obj:`models.entites.Role`) List of roles on behalf of which the task was commented
            subject (:obj:`str`): Updated task subject
        Attributes(Simple Task comment):
            reassign_to (:obj:`models.entities.Person`): Person to whom the task was reassigned
            participants_added (:obj:`list` of :obj:`models.entities.Person`): List of participants added to the task
            participants_removed (:obj:`list` of :obj:`models.entities.Person`): List of participants removed from the task
            due_date (:obj:`datetime`): Task due date
            due (:obj:`datetime`): Task due date with time
            duration (:obj:`int`): Task duration in minutes
            scheduled_date (:obj:`datetime`): task scheduled date
            cancel_schedule (:obj:`bool`): Flag indicating that schedule was cancelled for the task.
        Attributes(Form Task comment):
            field_updates (:obj:`list` of obj`models.entities.FormField`): List of updated field values
            approval_choice (:obj:`str`): Approval choice (approved/rejected/acknowledged)
            approval_step (:obj:`int`): Step number on which the task was approved
            reset_to_step (:obj:`int`) Step number on which the task was reseted
            changed_step (:obj:`int`) Step number on which the task was moved after comment
            approvals_added (:obj:`list` of :obj:`list` of :obj:`models.entities.Person`) List of approval steps added to the task
            approvals_removed (:obj:`list` of :obj:`list` of :obj:`models.entities.Person`) List of approval steps removed from the task
            approvals_rerequested (:obj:`list` of :obj:`list` of :obj:`models.entities.Person`) List of approval steps rerequested for the task
    """

    id = None
    text = None
    create_date = None
    author = None
    reassigned_to = None
    field_updates = None
    approval_choice = None
    approval_step = None
    reset_to_step = None
    approvals_added = None
    approvals_removed = None
    approvals_rerequested = None
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
    changed_step = None
    comment_as_roles = None
    subject = None
    @property
    def flat_field_updates(self):
        return _get_flat_fields(self.field_updates)

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'text' in kwargs:
            self.text = kwargs['text']
        if 'subject' in kwargs:
            self.subject = kwargs['subject']
        if 'create_date' in kwargs:
            self.create_date = _set_utc_timezone(datetime.strptime(kwargs['create_date'], DATE_TIME_FORMAT))
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
        if 'approvals_rerequested' in kwargs:
            self.approvals_rerequested = []
            for idx, approval in enumerate(kwargs['approvals_rerequested']):
                self.approvals_rerequested.append([])
                for curr_step in approval:
                    self.approvals_rerequested[idx].append(Approval(**curr_step))
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
            self.due = _set_utc_timezone(datetime.strptime(kwargs['due'], DATE_TIME_FORMAT))
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
        if 'approval_step' in kwargs:
            self.approval_step = kwargs['approval_step']
        if 'changed_step' in kwargs:
            self.changed_step = kwargs['changed_step']
        if 'comment_as_roles' in kwargs:
            self.comment_as_roles = []
            for role in kwargs['comment_as_roles']:
                self.comment_as_roles.append(Role(**role))

class Organization(object):
    """
        Organization
        
        Attributes:
            id (:obj:`int`): Organization id
            name (:obj:`str`): Organization name
            persons (:obj:`list` of :obj:`models.entities.Person`): List of persons in the organization
            roles (:obj:`list` of :obj:`models.entities.Role`): List of roles in the organization
    """

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
    """
        Role
        
        Attributes:
            id (:obj:`int`): Role id
            name (:obj:`str`): Role name
            member_ids (:obj:`list` of :obj:`int`): List of persons ids in the role
    """

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
    """
        Value of FormField catalog
        
        Attributes:
            item_id (:obj:`int`): Catalog item id
            values (:obj:`list` of :obj:`str`): List of catalog values
            headers (:obj:`list` of :obj:`str`): List of catalog headers
    """

    item_id = None
    values = None
    headers = None

    def __init__(self, **kwargs):
        if 'headers' in kwargs:
            self.headers = []
            for header in kwargs['headers']:
                self.headers.append(header)
        if 'item_id' in kwargs:
            self.item_id = kwargs['item_id']
        if 'values' in kwargs:
            self.values = []
            for value in kwargs['values']:
                self.values.append(value)

    @classmethod
    def fromliststr(cls, values):
        if not isinstance(values, list):
            raise TypeError('lst must be a list of str')
        for item in values:
            if not isinstance(item, str):
                raise TypeError('lst must be a list of str')
        values = {'values': values}
        return cls(**values)

class Table(list):
    """
        Value of FormField table
        List of `models.entities.TableRow`
    """

    def __init__(self, *args):
        list.__init__(self)
        for value in args:
            self.append(TableRow(**value))

class TableRow(object):
    """
        Table Row
        
        Attributes:
            row_id (:obj:`int`): Table row id
            cells (:obj:`list` of :obj:`models.entities.FormField`): List of row cells
            delete (:obj:`bool`): Flag indicating if table row should be deleted
    """

    row_id = None
    cells = None
    delete = None

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
        if 'delete' in kwargs:
            self.delete = kwargs['delete']
            if not isinstance(self.delete, bool):
                raise TypeError('delete must be a boolean')

class Title(object):
    """
        Value of FormField title
        
        Attributes:
            checkmark (:obj:`str`): checkmark value (checked/unchecked)
            fields (:obj:`list` of :obj:`models.entities.FormField`): List of title child fields
    """

    checkmark = None
    fields = None

    def __init__(self, **kwargs):
        if 'checkmark' in kwargs:
            self.checkmark = kwargs['checkmark']
        if 'fields' in kwargs:
            self.fields = []
            for field in kwargs['fields']:
                self.fields.append(FormField(**field))

class MultipleChoice(object):
    """
        Value of FormField multiple_choice
        
        Attributes:
            choice_ids (:obj:`list` of :obj:`int`): choice ids
            choice_names (:obj:`list` of :obj:`str`): choice names
            fields (:obj:`list` of :obj:`models.entities.FormField`): List of multiple choice child fields
            choice_id (:obj:`int`, deprecated): choice id
    """

    choice_id = None
    fields = None
    choice_ids = None
    choice_names = None

    def __init__(self, **kwargs):
        if 'choice_id' in kwargs:
            self.choice_id = kwargs['choice_id']
        if 'choice_ids' in kwargs:
            self.choice_ids = []
            for choice in kwargs['choice_ids']:
                self.choice_ids.append(choice)
        if 'choice_names' in kwargs:
            self.choice_names = []
            for choice in kwargs['choice_names']:
                self.choice_names.append(choice)
        if 'fields' in kwargs:
            self.fields = []
            for field in kwargs['fields']:
                self.fields.append(FormField(**field))

class Projects(object):
    """
        Value of FormField project
        
        Attributes:
            projects (:obj:`list` of :obj:`models.entities.Project`): List of projects
    """

    projects = None

    def __init__(self, **kwargs):
        if 'projects' in kwargs:
            self.projects = []
            for project in kwargs['projects']:
                self.projects.append(Project(**project))

class FormLink(object):
    """
        Value of FormField form_link
        
        Attributes:
            task_ids (:obj:`list` of :obj:`int`): List of task identifiers
            subject (:obj:`str`): task subjects
            task_id (:obj:`int`, deprecated): task identifier
    """

    task_id = None
    subject = None
    task_ids = None

    def __init__(self, **kwargs):
        if 'task_id' in kwargs:
            self.task_id = kwargs['task_id']
        if 'subject' in kwargs:
            self.subject = kwargs['subject']
        if 'task_ids' in kwargs:
            self.task_ids = []
            for task in kwargs['task_ids']:
                self.task_ids.append(task)

class Project(object):
    """
        Project
        
        Attributes:
            id (:obj:`int`): Project id
            name (:obj:`str`): Project name
            parent (:obj:`models.entities.Project`): Parent project
    """

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
    """
        Base form register filter. Should never be created explictly
    """

    def __init__(self, **kwargs):
        self.field_id = kwargs['field_id']
        self.operator = kwargs['operator']
        self.values = kwargs['values']

class EqualsFilter(FormRegisterFilter):
    """
        Form register equals filter
        
        Attributes:
            field_id (:obj:`int`): Form field id
            value (:obj:`str`): Form field value
    """

    def __init__(self, field_id, value):
        _validate_field_id(field_id)
        super(EqualsFilter, self).\
            __init__(field_id=field_id, operator='equals', values=_get_value(value))

class GreaterThanFilter(FormRegisterFilter):
    """
        Form register greater than filter
        
        Attributes:
            field_id (:obj:`int`): Form field id
            value (:obj:`str`): Form field value
    """

    def __init__(self, field_id, value):
        _validate_field_id(field_id)
        super(GreaterThanFilter, self).\
            __init__(field_id=field_id, operator='greater_than', values=_get_value(value))

class LessThanFilter(FormRegisterFilter):
    """
        Form register less than filter
        
        Attributes:
            field_id (:obj:`int`): Form field id
            value (:obj:`str`): Form field value
    """

    def __init__(self, field_id, value):
        _validate_field_id(field_id)
        super(LessThanFilter, self).\
            __init__(field_id=field_id, operator='less_than', values=_get_value(value))

class RangeFilter(FormRegisterFilter):
    """
        Form register range filter
        
        Attributes:
            field_id (:obj:`int`): Form field id
            value (:obj:`str`): Form field value
    """

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
    """
        Form register is in filter
        
        Attributes:
            field_id (:obj:`int`): Form field id
            value (:obj:`str`): Form field value
    """

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
    """
        task list
        
        Attributes:
            id (:obj:`int`): Task list id
            name (:obj:`str`): Task list name
            children (:obj:`models.entities.TaskList`): Task list children
    """

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

class CatalogHeader(object):
    """
        catalog header
        
        Attributes:
            name (:obj:`str`): Catalog header name
            type (:obj:`str`): Catalog header type (text/workflow)
    """

    name = None
    type = None

    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'type' in kwargs:
            self.type = kwargs['type']

def _get_value(value):
    if isinstance(value, datetime):
        return value.strftime(DATE_FORMAT)
    return value

def _validate_field_id(field_id):
    if not isinstance(field_id, int):
        raise TypeError('field_id must be valid int.')

def _create_field_value(field_type, value):
    if field_type in ['text', 'money', 'number', 'checkmark', 'email',
                      'phone', 'flag', 'step', 'status', 'note']:
        return value
    if field_type == 'time':
        return _set_utc_timezone(datetime.strptime(value, TIME_FORMAT).time())
    if field_type in ['date', 'create_date', 'due_date']:
        return _set_utc_timezone(datetime.strptime(value, DATE_FORMAT))
    if field_type == 'due_date_time':
        return _set_utc_timezone(datetime.strptime(value, DATE_TIME_FORMAT))
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
    if field_type == 'multiple_choice':
        return MultipleChoice(**value)
    if field_type == 'project':
        return Projects(**value)
    if field_type == 'form_link':
        return FormLink(**value)


def _get_flat_fields(fields):
    res = []
    if not fields:
        return res
    for field in fields:
        res.append(field)
        if (isinstance(field.value, Title) or isinstance(field.value, MultipleChoice)):
            res.extend(_get_flat_fields(field.value.fields))
        if (isinstance(field.value, Table)):
            for table_row in field.value:
                if table_row.cells:
                    res.extend(table_row.cells)
    return res

def _set_utc_timezone(time):
    if time.tzinfo is None:
        time = time.replace(tzinfo=timezone.utc)
    return time
    
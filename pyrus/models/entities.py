# pylint: disable=C0103
# pylint: disable=R0903
# pylint: disable=too-many-instance-attributes

from datetime import datetime
from datetime import timezone
from . import customhandlers
from . import constants


@customhandlers.FormFieldHandler.handles
class FormField:
    """
        Form field

        Attributes:
            id (:obj:`int`): Field id
            type (:obj:`str`): Field type
            name (:obj:`str`): Field name
            info (:obj:`models.entities.FormFieldInfo`): Additional field information
            value (:obj:`object`, optional): Field value
            duration (:obj:`int`, optional): Duration (returned if field type is 'due_date' or 'due_date_time')
            parent_id (:obj:`int`, optional) Parent field id (returned if field has parent)
            row_id (:obj:`int`, optional) Table row id (returned if field is in table)
            code (:obj:`str`): Code of the field
    """

    id = None
    type = None
    name = None
    info = None
    value = None
    duration = None
    parent_id = None
    row_id = None
    code = None

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
        if 'duration' in kwargs and self.type in ['due_date', 'due_date_time']:
            self.duration = kwargs['duration']
        if 'parent_id' in kwargs:
            self.parent_id = kwargs['parent_id']
        if 'row_id' in kwargs:
            self.row_id = kwargs['row_id']
        if 'code' in kwargs:
            self.code = kwargs['code']


class FormFieldInfo:
    """
        Additional form field information

        Attributes:
            required_step (:obj:`int`): Indicates the step number where the field becomes required for filling
            immutable_step (:obj:`int`): indicates the step number from which the user can't change the field value
            options (:obj:`list` of :obj:`models.entitites.ChoiceOption`): Choice options for multiple_choice field
            catalog_id (:obj:`int`): Catalog id for catalog field
            columns (:obj:`list` of :obj:`models.entitites.FormField`): Columns description for table field
            fields (:obj:`list` of :obj:`models.entitites.FormField`): Child fields description for title field
            decimal_places(:obj:`int`): Number of decimal places for number field
            multiple_choice (:obj:`bool`, optional): Flag indicating that mutliple values can be selected in Catalog field
            code (:obj:`str`): Code of the field
    """

    required_step = None
    immutable_step = None
    options = None
    catalog_id = None
    columns = None
    fields = None
    decimal_places = None
    multiple_choice = None
    code = None

    def __init__(self, **kwargs):
        if 'required_step' in kwargs:
            self.required_step = kwargs['required_step']
        if 'immutable_step' in kwargs:
            self.immutable_step = kwargs['immutable_step']
        if 'options' in kwargs:
            self.options = [ChoiceOption(**option) for option in kwargs['options']]
        if 'catalog_id' in kwargs:
            self.catalog_id = kwargs['catalog_id']
        if 'columns' in kwargs:
            self.columns = [FormField(**column) for column in kwargs['columns']]
        if 'fields' in kwargs:
            self.fields = [FormField(**field) for field in kwargs['fields']]
        if 'decimal_places' in kwargs:
            self.decimal_places = kwargs['decimal_places']
        if 'multiple_choice' in kwargs:
            self.multiple_choice = kwargs['multiple_choice']


class ChoiceOption:
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
            self.fields = [FormField(**field) for field in kwargs['fields']]
        if 'deleted' in kwargs:
            self.deleted = kwargs['deleted']
        if 'code' in kwargs:
            self.code = kwargs['code']


class TaskHeader:
    """
        Task header

        Attributes:
            id (:obj:`int`): Task id
            create_date (:obj:`datetime`): Task creation date
            last_modified_date (:obj:`datetime`): Task last modified date
            close_date (:obj:`datetime`): Task closing date
            author (:obj:`models.entities.Person`): Task author
            responsible (:obj:`models.entities.Person`): Task responsible
            due_date (:obj:`datetime`): Task due date
        Attributes(Simple Task):
            text (:obj:`str`): Task text
    """

    id = None
    text = None
    create_date = None
    last_modified_date = None
    author = None
    close_date = None
    responsible = None
    due_date = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'text' in kwargs:
            self.text = kwargs['text']
        if 'create_date' in kwargs:
            self.create_date = _set_utc_timezone(datetime.strptime(kwargs['create_date'], constants.DATE_TIME_FORMAT))
        if 'last_modified_date' in kwargs:
            self.last_modified_date = _set_utc_timezone(
                datetime.strptime(kwargs['last_modified_date'], constants.DATE_TIME_FORMAT))
        if 'author' in kwargs:
            self.author = Person(**kwargs['author'])
        if 'close_date' in kwargs:
            self.close_date = _set_utc_timezone(datetime.strptime(kwargs['close_date'], constants.DATE_TIME_FORMAT))
        if 'responsible' in kwargs:
            self.responsible = Person(**kwargs['responsible'])
        if 'due_date' in kwargs:
            self.due_date = datetime.strptime(kwargs['due_date'], constants.DATE_FORMAT)


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
            scheduled_date (:obj:`datetime`): task scheduled date
            scheduled_datetime_utc (:obj:`datetime`): task scheduled date with utc time
            subscribers (:obj:`list` of :obj:`models.entities.Subscriber`): List of task subscribers
            steps (:obj:`list` of :obj:`models.entities.TaskStep`): List of task steps
            due_date (:obj:`datetime`): Task due date
            due (:obj:`datetime`): Task due date with time
            duration (:obj:`int`): Task duration in minutes
        Attributes(Simple Task):
            text (:obj:`str`): Task text
            responsible (:obj:`models.entities.Person`): Task responsible
            participants (:obj:`list` of :obj:`models.entities.Person`): List of task participants
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
    subscribers = None
    participants = None
    scheduled_date = None
    scheduled_datetime_utc = None
    list_ids = None
    parent_task_id = None
    linked_task_ids = None
    last_note_id = None
    subject = None
    current_step = None

    @property
    def flat_fields(self):
        return _get_flat_fields(self.fields)

    def __init__(self, **kwargs):
        if 'subject' in kwargs:
            self.subject = kwargs['subject']
        if 'due_date' in kwargs:
            self.due_date = datetime.strptime(kwargs['due_date'], constants.DATE_FORMAT)
        if 'due' in kwargs:
            self.due = _set_utc_timezone(datetime.strptime(kwargs['due'], constants.DATE_TIME_FORMAT))
        if 'duration' in kwargs:
            self.duration = kwargs['duration']
        if 'scheduled_date' in kwargs:
            self.scheduled_date = datetime.strptime(kwargs['scheduled_date'], constants.DATE_FORMAT)
        if 'scheduled_datetime_utc' in kwargs:
            self.scheduled_datetime_utc = datetime.strptime(kwargs['scheduled_datetime_utc'],
                                                            constants.DATE_TIME_FORMAT)
        if 'form_id' in kwargs:
            self.form_id = kwargs['form_id']
        if 'attachments' in kwargs:
            self.attachments = [File(**attachment) for attachment in kwargs['attachments']]
        if 'parent_task_id' in kwargs:
            self.parent_task_id = kwargs['parent_task_id']
        if 'linked_task_ids' in kwargs:
            self.linked_task_ids = [linked_task_id for linked_task_id in kwargs['linked_task_ids']]
        if 'fields' in kwargs:
            self.fields = [FormField(**field) for field in kwargs['fields']]
        if 'approvals' in kwargs:
            self.approvals = []
            for idx, approval in enumerate(kwargs['approvals']):
                self.approvals.append([])
                for curr_step in approval:
                    approval = Approval(**curr_step)
                    approval.step = idx
                    self.approvals[idx].append(approval)
        if 'subscribers' in kwargs:
            self.subscribers = [Subscriber(**subscriber) for subscriber in kwargs['subscribers']]
        if 'participants' in kwargs:
            self.participants = [Person(**participant) for participant in kwargs['participants']]
        if 'list_ids' in kwargs:
            self.list_ids = [lst for lst in kwargs['list_ids']]
        if 'last_note_id' in kwargs:
            self.last_note_id = kwargs['last_note_id']
        if 'current_step' in kwargs:
            self.current_step = kwargs['current_step']
        if 'steps' in kwargs:
            self.steps = [TaskStep(**step) for step in kwargs['steps']]
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
            scheduled_date (:obj:`datetime`): task scheduled date
            scheduled_datetime_utc (:obj:`datetime`): task scheduled date with utc time
            subscribers (:obj:`list` of :obj:`models.entities.Subscriber`): List of task subscribers
            responsible (:obj:`models.entities.Person`): Task responsible
            due_date (:obj:`datetime`): Task due date
            due (:obj:`datetime`): Task due date with time
            duration (:obj:`int`): Task duration in minutes
        Attributes(Simple Task):
            text (:obj:`str`): Task text
            participants (:obj:`list` of :obj:`models.entities.Person`): List of task participants
        Attributes(Form Task):
            form_id (:obj:`int`): Form template id
            fields (:obj:`list` of obj`models.entities.FormField`): List of field values
            approvals (:obj:`list` of :obj:`list` of :obj:`models.entities.Person`) List of approval steps.
    """

    comments = None

    def __init__(self, **kwargs):
        if 'comments' in kwargs:
            self.comments = [TaskComment(**comment) for comment in kwargs['comments']]
        super(TaskWithComments, self).__init__(**kwargs)

class AnnouncementWithComments:
    """
        Announcement with comments

        Attributes:
            id (:obj:`int`): Announcement id
            create_date (:obj:`datetime`): Announcement creation date
            author (:obj:`models.entities.Person`): Announcement author
            attachments (:obj:`list` of :obj:`models.entities.File`): List of announcement attachments
            comments (:obj:`list` of :obj:`models.entities.AnnouncementComment`): List of announcement comments
            text (:obj:`str`): Announcement text
    
    """
    id = None
    create_date = None
    author = None
    attachments = None
    comments = None
    text = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'text' in kwargs:
            self.text = kwargs['text']
        if 'create_date' in kwargs:
            self.create_date = _set_utc_timezone(datetime.strptime(kwargs['create_date'], constants.DATE_TIME_FORMAT))
        if 'attachments' in kwargs:
            self.attachments = [File(**attachment) for attachment in kwargs['attachments']]
        if 'author' in kwargs:
            self.author = Person(**kwargs['author'])
        if 'comments' in kwargs:
            self.comments = [AnnouncementComment(**comment) for comment in kwargs['comments']]



class Person:
    """
        Person

        Attributes:
            id (:obj:`int`): Person's id
            first_name (:obj:`str`): Person's first name
            last_name (:obj:`str`): Person's last name
            email (:obj:`str`): Person's email
            status (:obj:`str`): Person's status
            avatar_id (:obj:`int`) Person's avatar ID
            external_avatar_id (:obj:`int`) Persons external avatar ID
            type (:obj:`str`): Person's type (user/bot/role)
            department_id (:obj:`int`): Person's department id
            department_name (:obj:`str`): Person's department
            phone (:obj:`str`): Person`s phone
            mobile_phone (:obj:`str`): Person`s mobile_phone
            position (:obj:`str`): Person`s position
    """

    id = None
    first_name = None
    last_name = None
    email = None
    status = None
    avatar_id = None
    external_avatar_id = None
    type = None
    department_id = None
    department_name = None
    phone = None
    mobile_phone = None
    position = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'first_name' in kwargs:
            self.first_name = kwargs['first_name']
        if 'last_name' in kwargs:
            self.last_name = kwargs['last_name']
        if 'email' in kwargs:
            self.email = kwargs['email']
        if 'status' in kwargs:
            self.status = kwargs['status']
        if 'avatar_id' in kwargs:
            self.avatar_id = kwargs['avatar_id']
        if 'external_avatar_id' in kwargs:
            self.external_avatar_id = kwargs['external_avatar_id']
        if 'type' in kwargs:
            self.type = kwargs['type']
        if 'department_id' in kwargs:
            self.department_id = kwargs['department_id']
        if 'department_name' in kwargs:
            self.department_name = kwargs['department_name']
        if 'phone' in kwargs:
            self.phone = kwargs['phone']
        if 'mobile_phone' in kwargs:
            self.mobile_phone = kwargs['mobile_phone']
        if 'position' in kwargs:
            self.position = kwargs['position']


class File:
    """
        File

        Attributes:
            id (:obj:`int`): File id
            name (:obj:`str`): File name
            size (:obj:`int`): File size in bytes
            md5 (:obj:`str`): File md5 hash
            url (:obj:`str`): Url to download the file
            version (:obj:`int`): File version
            root_id (:obj:`int`): Root file id
    """

    id = None
    name = None
    size = None
    md5 = None
    url = None
    version = None
    root_id = None

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
        if 'root_id' in kwargs:
            self.root_id = kwargs['root_id']


class Approval:
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


class Subscriber:
    """
        Subscriber

        Attributes:
            person (:obj:`entities.models.Person`): Subscriber person
            approval_choice (:obj:`str`): Approval choice (approved/rejected/revoked/acknowledged)
    """

    person = None
    approval_choice = None

    def __init__(self, **kwargs):
        if 'person' in kwargs:
            self.person = Person(**kwargs['person'])
        if 'approval_choice' in kwargs:
            self.approval_choice = kwargs['approval_choice']


class TaskComment:
    """
        Task comment

        Attributes:
            id (:obj:`int`): Comment id
            text (:obj:`str`): Comment text
            mentions (:obj:`list` of :obj:`int`) Mentioned users in comment text
            create_date (:obj:`datetime`): Comment creation date
            author (:obj:`models.entities.Person`): Comment author
            attachments (:obj:`list` of :obj:`models.entities.File`): List of comment attachments
            action (:obj:`str`): Activity action (finished/reopened)
            added_list_ids (:obj:`list` of :obj:`int`): List of list identifiers to which the task was added
            removed_list_ids (:obj:`list` of :obj:`int`): List of list identifiers from the task was removed
            comment_as_roles (:obj:`list` of :obj:`models.entites.Role`) List of roles on behalf of which the task was commented
            subject (:obj:`str`): Updated task subject
            scheduled_date (:obj:`datetime`): task scheduled date
            scheduled_datetime_utc (:obj:`datetime`): task scheduled date with utc time
            cancel_schedule (:obj:`bool`): Flag indicating that schedule was cancelled for the task.
            spent_minutes (:obj:`int`): Spent time in minutes
            subscribers_added (:obj:`list` of :obj:`models.entities.Person`) List of subscribers added to the task
            subscribers_removed (:obj:`list` of :obj:`models.entities.Person`) List of subscribers removed from the task
            subscribers_rerequested (:obj:`list` of :obj:`models.entities.Person`) List of subscribers rerequested for the task
            skip_satisfaction (:obj:`bool`, optional): Flag indicating that user satisfaction poll should be skipped
            skip_notification (:obj:`bool`, optional): Flag indicating that users notification should be skipped
            skip_auto_reopen (:obj:`bool`, optional): Flag indicating that task reopening should be skipped (only affects closed tasks)
            reply_note_id (:obj:`int`, optional): Id of the comment that was replied to
            due_date (:obj:`datetime`): Task due date
            due (:obj:`datetime`): Task due date with time
            duration (:obj:`int`): Task duration in minutes
        Attributes(Simple Task comment):
            reassign_to (:obj:`models.entities.Person`): Person to whom the task was reassigned
            participants_added (:obj:`list` of :obj:`models.entities.Person`): List of participants added to the task
            participants_removed (:obj:`list` of :obj:`models.entities.Person`): List of participants removed from the task
        Attributes(Form Task comment):
            field_updates (:obj:`list` of obj`models.entities.FormField`): List of updated field values
            approval_choice (:obj:`str`): Approval choice (approved/rejected/acknowledged)
            approval_step (:obj:`int`): Step number on which the task was approved
            reset_to_step (:obj:`int`) Step number on which the task was reseted
            changed_step (:obj:`int`) Step number on which the task was moved after comment
            approvals_added (:obj:`list` of :obj:`list` of :obj:`models.entities.Person`) List of approval steps added to the task
            approvals_removed (:obj:`list` of :obj:`list` of :obj:`models.entities.Person`) List of approval steps removed from the task
            approvals_rerequested (:obj:`list` of :obj:`list` of :obj:`models.entities.Person`) List of approval steps rerequested for the task
            channel (:obj:`models.entities.Channel`): External notification
    """

    id = None
    text = None
    mentions = None
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
    subscribers_added = None
    subscribers_removed = None
    subscribers_rerequested = None
    participants_added = None
    participants_removed = None
    due_date = None
    due = None
    duration = None
    attachments = None
    action = None
    scheduled_date = None
    scheduled_datetime_utc = None
    cancel_schedule = None
    added_list_ids = None
    removed_list_ids = None
    changed_step = None
    comment_as_roles = None
    subject = None
    channel = None
    spent_minutes = None
    skip_satisfaction = None
    reply_note_id = None
    skip_notification = None
    skip_auto_reopen = None

    @property
    def flat_field_updates(self):
        return _get_flat_fields(self.field_updates)

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'text' in kwargs:
            self.text = kwargs['text']
        if 'mentions' in kwargs:
            self.mentions = kwargs['mentions']
        if 'subject' in kwargs:
            self.subject = kwargs['subject']
        if 'create_date' in kwargs:
            self.create_date = _set_utc_timezone(datetime.strptime(kwargs['create_date'], constants.DATE_TIME_FORMAT))
        if 'author' in kwargs:
            self.author = Person(**kwargs['author'])
        if 'reassigned_to' in kwargs:
            self.reassigned_to = Person(**kwargs['reassigned_to'])
        if 'field_updates' in kwargs:
            self.field_updates = [FormField(**field) for field in kwargs['field_updates']]
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
        if 'subscribers_added' in kwargs:
            self.subscribers_added = [Person(**subscriber) for subscriber in kwargs['subscribers_added']]
        if 'subscribers_removed' in kwargs:
            self.subscribers_removed = [Person(**subscriber) for subscriber in kwargs['subscribers_removed']]
        if 'subscribers_rerequested' in kwargs:
            self.subscribers_rerequested = [Person(**subscriber) for subscriber in kwargs['subscribers_rerequested']]
        if 'participants_added' in kwargs:
            self.participants_added = [Person(**participant) for participant in kwargs['participants_added']]
        if 'participants_removed' in kwargs:
            self.participants_removed = [Person(**participant) for participant in kwargs['participants_removed']]
        if 'due_date' in kwargs:
            self.due_date = datetime.strptime(kwargs['due_date'], constants.DATE_FORMAT)
        if 'due' in kwargs:
            self.due = _set_utc_timezone(datetime.strptime(kwargs['due'], constants.DATE_TIME_FORMAT))
        if 'duration' in kwargs:
            self.duration = kwargs['duration']
        if 'attachments' in kwargs:
            self.attachments = [File(**attachment) for attachment in kwargs['attachments']]
        if 'action' in kwargs:
            self.action = kwargs['action']
        if 'scheduled_date' in kwargs:
            self.scheduled_date = datetime.strptime(kwargs['scheduled_date'], constants.DATE_FORMAT)
        if 'scheduled_datetime_utc' in kwargs:
            self.scheduled_datetime_utc = datetime.strptime(kwargs['scheduled_datetime_utc'],
                                                            constants.DATE_TIME_FORMAT)
        if 'cancel_schedule' in kwargs:
            self.cancel_schedule = kwargs['cancel_schedule']
        if 'added_list_ids' in kwargs:
            self.added_list_ids = [lst for lst in kwargs['added_list_ids']]
        if 'removed_list_ids' in kwargs:
            self.removed_list_ids = [lst for lst in kwargs['removed_list_ids']]
        if 'approval_step' in kwargs:
            self.approval_step = kwargs['approval_step']
        if 'changed_step' in kwargs:
            self.changed_step = kwargs['changed_step']
        if 'comment_as_roles' in kwargs:
            self.comment_as_roles = [Role(**role) for role in kwargs['comment_as_roles']]
        if 'channel' in kwargs:
            self.channel = Channel(**kwargs['channel'])
        if 'spent_minutes' in kwargs:
            self.spent_minutes = kwargs['spent_minutes']
        if 'skip_satisfaction' in kwargs:
            self.skip_satisfaction = kwargs['skip_satisfaction']
        if 'reply_note_id' in kwargs:
            self.reply_note_id = kwargs['reply_note_id']
        if 'skip_notification' in kwargs:
            self.skip_notification = kwargs['skip_notification']
        if 'skip_auto_reopen' in kwargs:
            self.skip_auto_reopen = kwargs['skip_auto_reopen']

class TaskStep:
    """
        Task step

        Attributes:
            step (:obj:`int`): step number
            name (:obj:`str`): step name text
            elapsed_time (:obj:`int`): elapsed time at step in millisecond
    """

    step = None
    name = None
    elapsed_time = None

    def __init__(self, **kwargs):
        if 'step' in kwargs:
            self.step = kwargs['step']
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'elapsed_time' in kwargs:
            self.elapsed_time = kwargs['elapsed_time']

class AnnouncementComment:
    """
        Announcement comment

        Attributes:
            id (:obj:`int`): Comment id
            text (:obj:`str`): Comment text
            create_date (:obj:`datetime`): Comment creation date
            author (:obj:`models.entities.Person`): Comment author
            attachments (:obj:`list` of :obj:`models.entities.File`): List of comment attachments
    """

    id = None
    text = None
    create_date = None
    author = None
    attachments = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'text' in kwargs:
            self.text = kwargs['text']
        if 'create_date' in kwargs:
            self.create_date = _set_utc_timezone(datetime.strptime(kwargs['create_date'], constants.DATE_TIME_FORMAT))
        if 'author' in kwargs:
            self.author = Person(**kwargs['author'])
        if 'attachments' in kwargs:
            self.attachments = [File(**attachment) for attachment in kwargs['attachments']]

class Organization:
    """
        Organization

        Attributes:
            organization_id (:obj:`int`): Organization id
            name (:obj:`str`): Organization name
            persons (:obj:`list` of :obj:`models.entities.Person`): List of persons in the organization
            roles (:obj:`list` of :obj:`models.entities.Role`): List of roles in the organization
            department_catalog_id (:obj:`int`): Department catalog id
    """

    organization_id = None
    name = None
    persons = None
    roles = None
    department_catalog_id = None

    def __init__(self, **kwargs):
        if 'organization_id' in kwargs:
            self.organization_id = kwargs['organization_id']
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'persons' in kwargs:
            self.persons = [Person(**person) for person in kwargs['persons']]
        if 'roles' in kwargs:
            self.roles = [Role(**role) for role in kwargs['roles']]
        if 'department_catalog_id' in kwargs:
            self.department_catalog_id = kwargs['department_catalog_id']


class Role:
    """
        Role

        Attributes:
            id (:obj:`int`): Role id
            name (:obj:`str`): Role name
            member_ids (:obj:`list` of :obj:`int`): List of persons ids in the role
            banned(:obj:`bool`): Is the role banned
            fired(:obj:`bool`): Is the role fired
            avatar_id (:obj:`int`) Roles avatar ID
            external_avatar_id (:obj:`int`) Roles external avatar ID
    """

    id = None
    name = None
    member_ids = None
    banned = None
    fired = None
    avatar_id = None
    external_avatar_id = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'member_ids' in kwargs:
            self.member_ids = [member_id for member_id in kwargs['member_ids']]
        if 'banned' in kwargs:
            self.banned = kwargs['banned']
        if 'fired' in kwargs:
            self.fired = kwargs['fired']
        if 'avatar_id' in kwargs:
            self.avatar_id = kwargs['avatar_id']
        if 'external_avatar_id' in kwargs:
            self.external_avatar_id = kwargs['external_avatar_id']

class CatalogItem:
    """
        Value of FormField catalog

        Attributes:
            item_id (:obj:`int`, deprecated): Catalog item id
            values (:obj:`list` of :obj:`str`, deprecated): List of catalog values
            headers (:obj:`list` of :obj:`str`): List of catalog headers
            item_ids (:obj:`list` of :obj:`int`m): List of catalog item ids
            rows (:obj:`list` of :obj:`list` of :obj:`str`): List of catalog rows
    """

    item_id = None
    values = None
    headers = None

    def __init__(self, **kwargs):
        if 'headers' in kwargs:
            self.headers = [header for header in kwargs['headers']]

        if 'item_ids' in kwargs:
            self.item_ids = [_id for _id in kwargs['item_ids']]
            if len(self.item_ids) == 1:
                self.item_id = self.item_ids[0]
        elif 'item_id' in kwargs:
            self.item_id = kwargs['item_id']
            self.item_ids = [kwargs['item_id']]

        if 'rows' in kwargs:
            self.rows = []
            for row in kwargs['rows']:
                row_copy = []
                for value in row:
                    row_copy.append(value)
                self.rows.append(row_copy)
            if len(self.rows) == 1:
                self.values = self.rows[0].copy()
        elif 'values' in kwargs:
            self.values = [value for value in kwargs['values']]
            self.rows = [self.values.copy()]

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


class TableRow:
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
    deleted = None

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
        if 'deleted' in kwargs:
            self.deleted = kwargs['deleted']
            if not isinstance(self.deleted, bool):
                raise TypeError('deleted must be a boolean')


class Title:
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
            self.fields = [FormField(**field) for field in kwargs['fields']]


class MultipleChoice:
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
            self.choice_ids = [choice for choice in kwargs['choice_ids']]
        if 'choice_names' in kwargs:
            self.choice_names = [choice for choice in kwargs['choice_names']]
        if 'fields' in kwargs:
            self.fields = [FormField(**field) for field in kwargs['fields']]


class Projects:
    """
        Value of FormField project

        Attributes:
            projects (:obj:`list` of :obj:`models.entities.Project`): List of projects
    """

    projects = None

    def __init__(self, **kwargs):
        if 'projects' in kwargs:
            self.projects = [Project(**project) for project in kwargs['projects']]


class FormLink:
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
            self.task_ids = [task for task in kwargs['task_ids']]


class Project:
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


class FormRegisterSort:
    """
        Form register sort (currently only works by task Ids)
        Attributes:
            by_task_id (:obj:`bool`): Is sort order by task Id
    """

    def __init__(self, by_task_id = True):
        self.type = by_task_id and 'tsk' or None


class BaseFilter:
    """
        Base filter. Should never be created explictly
    """

    def __init__(self, **kwargs):
        self.operator = kwargs['operator']
        self.values = kwargs['values']

class FormRegisterTaskIdFilter(BaseFilter):
    """
        Base form register task id filter. Should never be created explictly
    """

    def __init__(self, **kwargs):
        super(FormRegisterTaskIdFilter, self).__init__(**kwargs)



class FormRegisterFilter(BaseFilter):
    """
        Base form register filter. Should never be created explictly
    """

    def __init__(self, **kwargs):
        super(FormRegisterFilter, self).__init__(**kwargs)
        self.field_id = kwargs['field_id']


class EqualsFilter(FormRegisterFilter):
    """
        Form register equals filter

        Attributes:
            field_id (:obj:`int`): Form field id
            value (:obj:`str`): Form field value
    """

    def __init__(self, field_id, value):
        _validate_field_id(field_id)
        super(EqualsFilter, self). \
            __init__(field_id=field_id, operator='equals', values=_get_value(value))

class EqualsTaskIdFilter(FormRegisterTaskIdFilter):
    """
        Form register task id equals filter

        Attributes:
            value (:obj:`str`): Form field value
    """

    def __init__(self, value):
        super(EqualsTaskIdFilter, self). \
            __init__(operator='equals', values=_get_value(value))


class GreaterThanFilter(FormRegisterFilter):
    """
        Form register greater than filter

        Attributes:
            field_id (:obj:`int`): Form field id
            value (:obj:`str`): Form field value
    """

    def __init__(self, field_id, value):
        _validate_field_id(field_id)
        super(GreaterThanFilter, self). \
            __init__(field_id=field_id, operator='greater_than', values=_get_value(value))

class GreaterThanTaskIdFilter(FormRegisterTaskIdFilter):
    """
        Form register greater than task id filter

        Attributes:
            value (:obj:`str`): Form field value
    """

    def __init__(self, value):
        super(GreaterThanTaskIdFilter, self). \
            __init__(operator='greater_than', values=_get_value(value))


class LessThanFilter(FormRegisterFilter):
    """
        Form register less than filter

        Attributes:
            field_id (:obj:`int`): Form field id
            value (:obj:`str`): Form field value
    """

    def __init__(self, field_id, value):
        _validate_field_id(field_id)
        super(LessThanFilter, self). \
            __init__(field_id=field_id, operator='less_than', values=_get_value(value))


class LessThanTaskIdFilter(FormRegisterTaskIdFilter):
    """
        Form register task id less than filter

        Attributes:
            value (:obj:`str`): Form field value
    """

    def __init__(self, value):
        super(LessThanTaskIdFilter, self). \
            __init__(operator='less_than', values=_get_value(value))


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
        formated_values = [_get_value(value) for value in values]
        super(RangeFilter, self). \
            __init__(field_id=field_id, operator='range', values=formated_values)

class RangeTaskIdFilter(FormRegisterTaskIdFilter):
    """
        Form register range task id filter

        Attributes:
            value (:obj:`str`): Form field value
    """

    def __init__(self, values):
        if not isinstance(values, list):
            raise TypeError('values must be a list.')
        if len(values) != 2:
            raise TypeError('values length must be equal 2.')
        formated_values = [_get_value(value) for value in values]
        super(RangeTaskIdFilter, self). \
            __init__(operator='range', values=formated_values)


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
        formated_values = [_get_value(value) for value in values]
        super(IsInFilter, self). \
            __init__(field_id=field_id, operator='is_in', values=formated_values)

class IsInTaskIdFilter(FormRegisterTaskIdFilter):
    """
        Form register is in task id filter

        Attributes:s
            value (:obj:`str`): Form field value
    """

    def __init__(self, values):
        if not isinstance(values, list):
            raise TypeError('values must be a list.')
        formated_values = [_get_value(value) for value in values]
        super(IsInTaskIdFilter, self). \
            __init__(operator='is_in', values=formated_values)


class IsEmptyFilter(FormRegisterFilter):
    """
        Form register is empty filter

        Attributes:
            field_id (:obj:`int`): Form field id
    """

    def __init__(self, field_id):
        _validate_field_id(field_id)
        super(IsEmptyFilter, self). \
            __init__(field_id=field_id, operator='is_empty', values=[])


class TaskList:
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
            self.children = [TaskList(**child) for child in kwargs['children']]


class CatalogHeader:
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
        return value.strftime(constants.DATE_FORMAT)
    return value


def _validate_field_id(field_id):
    if not isinstance(field_id, int):
        raise TypeError('field_id must be valid int.')


def _create_field_value(field_type, value):
    if field_type in ['text', 'money', 'number', 'checkmark', 'email',
                      'phone', 'flag', 'step', 'status', 'note']:
        return value
    if field_type == 'time':
        if isinstance(value, datetime):
            return value
        return _set_utc_timezone(datetime.strptime(value, constants.TIME_FORMAT).time())
    if field_type in ['date', 'creation_date', 'due_date']:
        if isinstance(value, datetime):
            return value
        return _set_utc_timezone(datetime.strptime(value, constants.DATE_FORMAT))
    if field_type == 'due_date_time':
        if isinstance(value, datetime):
            return value
        return _set_utc_timezone(datetime.strptime(value, constants.DATE_TIME_FORMAT))
    if field_type == 'catalog':
        return CatalogItem(**value)
    if field_type == 'file':
        return [File(**file) for file in value]
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


class NewFile:
    """
        Attachment definition

        Attributes:
            guid (:obj:`str`): Uploaded file GUID
            root_id (:obj:`int`): Existing file ID to create new version (optional)
            
            attachment_id (:obj:`int`): Existing file ID
            
            url (:obj:`str`): Existing file URL
            name (:obj:`str`): Link name (optional)
    """

    guid = None
    root_id = None
    attachment_id = None
    url = None
    name = None

    def __init__(self, **kwargs):
        if 'guid' in kwargs:
            self.guid = kwargs['guid']
        if 'root_id' in kwargs:
            self.root_id = kwargs['root_id']
        if 'attachment_id' in kwargs:
            self.attachment_id = kwargs['attachment_id']
        if 'url' in kwargs:
            self.url = kwargs['url']
        if 'name' in kwargs:
            self.name = kwargs['name']


@customhandlers.ChannelHandler.handles
class Channel:
    """
        Channel

        Attributes:
            type (:obj:`str`): Channel type (email, telegram, web, facebook, vk, viber, mobile_app, web_widget, moy_sklad, zadarma, amo_crm, beeline, api_telephony, zoom, instagram, private_channel, web_form, whats_app, sms, custom)
            to (:obj:`models.entities.ChannelUser`): Notification recipient
            sender (:obj:`models.entities.ChannelUser`): Notification sender
            phone (:obj:`str`): Phone number for send sms
    """

    type = None
    to = None
    sender = None
    phone = None

    def __init__(self, **kwargs):
        if 'type' in kwargs:
            self.type = kwargs['type']
        if 'to' in kwargs:
            self.to = kwargs['to']
        if 'from' in kwargs:
            self.sender = kwargs['from']
        if 'phone' in kwargs:
            self.phone = kwargs['phone']


class CatalogValue:
    """
        Catalog field value

        Attributes:
            item_id (:obj:`int`, deprecated): Catalog item id
            item_name (:obj:`str`, deprecated): Catalog item name
            item_ids (:obj:`list` of :obj:`int`): List of catalog item ids
            item_names (:obj:`list` of :obj:`str`): List of catalog item names
    """

    def __init__(self, item_id=None, item_name=None, item_ids=None, item_names=None):
        if item_id:
            self.item_id = item_id
        if item_name:
            self.item_name = item_name
        if item_ids:
            self.item_ids = item_ids
        if item_names:
            self.item_names = item_names

class MeetingJoinParameters:
    """
        Meeting join parameters
    
        Attributes:
            url (:obj:`str`): Meeting join URL
            external_id (:obj:`str`): Meeting join id
            password (:obj:`str`): Meeting join password
    """

    url = None
    external_id = None
    password = None

    def __init__(self, **kwargs):
        if 'url' in kwargs:
            self.url = kwargs['url']
        if 'external_id' in kwargs:
            self.external_id = kwargs['external_id']
        if 'password' in kwargs:
            self.password = kwargs['password']

class Meeting:
    """
        Meeting

        Attributes:
            id (:obj:`int`): Meeting id
            type (:obj:`str`): Meeting type
            start_time (:obj:`datetime`): Meeting start time
            duration (:obj:`int`): Meeting duration in minutes
            join_parameters (:obj:`models.entities.MeetingJoinParameters`): Meeting join parameters
            creator_id (:obj:`int`): Meeting creator person id
            task_id (:obj:`int`): Task id
            shared_calendar_event_id (:obj:`str`): Unique identifier for external users
            shared_to_email (:obj:`bool`): Flag indication that a notification has been sent regarding the latest meeting change
            deleted (:obj:`bool`): Is meeting deleted
    """

    id = None
    type = None
    start_time = None
    duration = None
    creator_id = None
    task_id = None
    shared_calendar_event_id = None
    shared_to_email = None
    deleted = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'type' in kwargs:
            self.type = kwargs['type']
        if 'start_time' in kwargs:
            self.start_time = _set_utc_timezone(datetime.strptime(kwargs['start_time'], constants.DATE_TIME_FORMAT))
        if 'duration' in kwargs:
            self.duration = kwargs['duration']
        if 'join_parameters' in kwargs:
            self.join_parameters = MeetingJoinParameters(**kwargs['join_parameters'])
        if 'creator_id' in kwargs:
            self.creator_id = kwargs['creator_id']
        if 'task_id' in kwargs:
            self.task_id = kwargs['task_id']
        if 'shared_calendar_event_id' in kwargs:
            self.shared_calendar_event_id = kwargs['shared_calendar_event_id']
        if 'shared_to_email' in kwargs:
            self.shared_to_email = kwargs['shared_to_email']
        if 'deleted' in kwargs:
            self.deleted = kwargs['deleted']

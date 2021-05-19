from datetime import datetime
from . import entities
from . import constants


class FormRegisterRequest(object):
    """
        FormRegisterRequest
        
        Args:
            steps (:obj:`list` of :obj:`int`, optional): List of step numbers. Only tasks on the specified steps will be returned
            include_archived (:obj:`bool`, optional): Flag indicating if we need to include archived tasks to the response. False by default
            filters (:obj:`list` of :obj:`models.entities.FormRegisterFilter`, optional): List of form field filters
            modified_before (:obj:`datetime`, optional): Include only tasks that were modified before specified date
            modified_after (:obj:`datetime`, optional): Include only tasks that were modified after specified date
            closed_before (:obj:`datetime`, optional): Include only tasks that were closed before specified date
            closed_after (:obj:`datetime`, optional): Include only tasks that were closed after specified date
            created_before (:obj:`datetime`, optional): Include only tasks that were created before specified date
            created_after (:obj:`datetime`, optional): Include only tasks that were created after specified date
            field_ids (:obj:`list` of :obj:`int`, optional): List of field ids. Only specified fields will be returned in the response. Order is preserved
            format (:obj:`str`, optional): Response format (json/csv). json by default
            delimiter (:obj:`str`, optional): Csv delimiter. Applicable only for csv format
            simple_format (:obj:`bool`, optional): Returns csv in simple for parsing format. Applicable only for csv format
            encoding (:obj:`str`, optional): Response encoding. Applicable only for csv format
    """

    def __init__(self, steps=None, include_archived=None, filters=None, modified_before=None, modified_after=None,
                 field_ids=None, format=None, delimiter=None, simple_format=None, encoding=None,
                 closed_before=None, closed_after=None, created_before=None, created_after=None):
        if steps:
            if not isinstance(steps, list):
                raise TypeError('steps must be a list of int')
            for item in steps:
                if not isinstance(item, int):
                    raise TypeError('steps must be a list of int')
            self.steps = steps

        if include_archived:
            if not isinstance(include_archived, bool):
                raise TypeError('include_archived must be bool')
            self.include_archived = include_archived

        if modified_before:
            self.modified_before = _date_to_str(modified_before, 'modified_before')
        if modified_after:
            self.modified_after = _date_to_str(modified_after, 'modified_after')
        if closed_before:
            self.closed_before = _date_to_str(closed_before, 'closed_before')
        if closed_after:
            self.closed_after = _date_to_str(closed_after, 'closed_after')
        if created_before:
            self.created_before = _date_to_str(created_before, 'created_before')
        if created_after:
            self.created_after = _date_to_str(created_after, 'created_after')

        if filters:
            if not isinstance(filters, list):
                raise TypeError('filters must be a list of entities.FormRegisterFilter')
            for fltr in filters:
                if not isinstance(fltr, entities.FormRegisterFilter):
                    raise TypeError('filters must be a list of entities.FormRegisterFilter')
                if fltr.operator == 'equals':
                    setattr(self, 'fld{}'.format(fltr.field_id), fltr.values)
                if fltr.operator == 'greater_than':
                    setattr(self, 'fld{}'.format(fltr.field_id), 'gt{}'.format(fltr.values))
                if fltr.operator == 'less_than':
                    setattr(self, 'fld{}'.format(fltr.field_id), 'lt{}'.format(fltr.values))
                if fltr.operator == 'range':
                    setattr(self, 'fld{}'.format(fltr.field_id), 'gt{},lt{}'.format(*fltr.values))
                if fltr.operator == 'is_in':
                    setattr(self, 'fld{}'.format(fltr.field_id), ",".join(fltr.values))

        if field_ids:
            if not isinstance(field_ids, list):
                raise TypeError('field_ids must be a list of int')
            for field_id in field_ids:
                if not isinstance(field_id, int):
                    raise TypeError('field_ids must be a list of int')
            self.field_ids = field_ids

        if format:
            if not isinstance(format, str):
                raise TypeError('format must be an instance of str')
            if format != "json" and format != "csv":
                raise TypeError('format must "json" or "csv"')
            self.format = format

        if delimiter:
            if not isinstance(delimiter, str):
                raise TypeError('delimiter must be a string')
            self.delimiter = delimiter

        if simple_format:
            if not isinstance(simple_format, bool):
                raise TypeError('simple_format must be a bool')
            self.simple_format = simple_format

        if encoding:
            if not isinstance(encoding, str):
                raise TypeError('encoding must be a string')
            self.encoding = encoding


class TaskCommentRequest(object):
    """
        TaskCommentRequest
        
        Args:
            text (:obj:`str`, optional): Comment text
            action (:obj:`str`, optional): Activity action (finished/reopened)
            attachments (:obj:`list` of :obj:`str` or :obj:`models.entities.NewFile`, optional): List of files to attach to the task
            added_list_ids (:obj:`list` of :obj:`int`, optional): List of list identifiers to which you want to add the task
            removed_list_ids (:obj:`list` of :obj:`int`, optional): List of list identifiers from which you want to remove the task
            scheduled_date (:obj:`datetime`, optional): task scheduled date
            scheduled_datetime_utc (:obj:`datetime`, optional): task scheduled date with utc time
            cancel_schedule (:obj:`bool`, optional): Flag indicating that schedule should be cancelled. The task will be moved to the inbox
            spent_minutes (:obj:`int`, optional): Spent time in minutes
            subscribers_added (:obj:`list` of :obj:`models.entities.Person`, optional): List of subscribers to add to the task
            subscribers_removed (:obj:`list` of :obj:`models.entities.Person`, optional): List of subscribers to remove from the task
            subscribers_rerequested (:obj:`list` of :obj:`models.entities.Person`, optional): List of subscribers to rerequest for the task
        Args(Simple task comment):
            participants_added (:obj:`list` of :obj:`models.entities.Person`, optional): List of participants to add to the task
            participants_removed (:obj:`list` of :obj:`models.entities.Person`, optional): List of participants to remove from the task
            reassign_to (:obj:`models.entities.Person`, optional): new responsible for the task
            due (:obj:`datetime`, optional): task due date with time (either due_date or due can be used)
            due_date (:obj:`datetime`, optional): task due date (either due_date or due can be used)
            duration (:obj:`int`, optional): duration of the event in minutes (it can only be used with due)
            subject (:obj:`str`, optional): New task subject
        Args(Form task comment):
            approval_choice (:obj:`str`, optional): Approval choice (approved/rejected/acknowledged)
            approval_steps (:obj:`list` of :obj:`int`, optional): Indicates for which steps approval_choice must be applied. By default: current step
            field_updates (:obj:`list` of :obj:`models.entities.FormField`, optional): List of field values to update
            approvals_added (:obj:`list` of :obj:`list` of :obj:`models.entities.Person`, optional) List of approval steps to add to the task
            approvals_removed (:obj:`list` of :obj:`list` of :obj:`models.entities.Person`, optional) List of approval steps to remove from the task
            approvals_rerequested (:obj:`list` of :obj:`list` of :obj:`models.entities.Person`, optional) List of approval steps to rerequest for the task
            channel (:obj:`str`) External channel to send notification (email, telegram, web, facebook, vk, viber, mobile_app, web_widget, moy_sklad, zadarma, amo_crm, instagram)
    """

    def __init__(self, text=None, approval_choice=None, approval_steps=None, action=None,
                 attachments=None, field_updates=None, approvals_added=None,
                 participants_added=None, reassign_to=None, due=None, due_date=None,
                 duration=None, scheduled_date=None, scheduled_datetime_utc=None,
                 cancel_schedule=None, added_list_ids=None, removed_list_ids=None,
                 approvals_removed=None, approvals_rerequested=None, subscribers_added=None, subscribers_removed=None,
                 subscribers_rerequested=None, subject=None,
                 participants_removed=None, channel=None, spent_minutes=None):
        if text:
            self.text = text
        if subject:
            self.subject = subject
        if approval_choice:
            if approval_choice not in ['approved', 'rejected', 'revoked', 'acknowledged']:
                raise TypeError(
                    'approval_choice can only be \'approved\', \'rejected\', \'acknowledged\', or \'revoked\'')
            self.approval_choice = approval_choice
        if action:
            if action not in ['finished', 'reopened']:
                raise TypeError('action can only be \'finished\' or \'reopened\'')
            self.action = action
        if reassign_to:
            if isinstance(reassign_to, entities.Person):
                self.reassign_to = reassign_to
            elif isinstance(reassign_to, int):
                self.reassign_to = entities.Person(id=reassign_to)
            else:
                self.reassign_to = entities.Person(email=reassign_to)
        if attachments:
            if not isinstance(attachments, list):
                raise TypeError('attachments must be a list')
            self.attachments = []
            for attachment in attachments:
                self.attachments.append(attachment)
        if approvals_added:
            if not isinstance(approvals_added, list):
                raise TypeError('approvals_added must be a list')
            self.approvals_added = []
            for idx, approval_step in enumerate(approvals_added):
                if not isinstance(approval_step, list):
                    raise TypeError('approval_step must be a list of persons, person ids'
                                    ', or person emails')
                self.approvals_added.append([])
                for person in approval_step:
                    if isinstance(person, entities.Person):
                        self.approvals_added[idx].append(person)
                    elif isinstance(person, int):
                        self.approvals_added[idx].append(entities.Person(id=person))
                    else:
                        self.approvals_added[idx].append(entities.Person(email=person))
        if approvals_removed:
            if not isinstance(approvals_removed, list):
                raise TypeError('approvals_removed must be a list')
            self.approvals_removed = []
            for idx, approval_step in enumerate(approvals_removed):
                if not isinstance(approval_step, list):
                    raise TypeError('approval_step must be a list of persons, person ids'
                                    ', or person emails')
                self.approvals_removed.append([])
                for person in approval_step:
                    if isinstance(person, entities.Person):
                        self.approvals_removed[idx].append(person)
                    elif isinstance(person, int):
                        self.approvals_removed[idx].append(entities.Person(id=person))
                    else:
                        self.approvals_removed[idx].append(entities.Person(email=person))
        if approvals_rerequested:
            if not isinstance(approvals_rerequested, list):
                raise TypeError('approvals_rerequested must be a list')
            self.approvals_rerequested = []
            for idx, approval_step in enumerate(approvals_rerequested):
                if not isinstance(approval_step, list):
                    raise TypeError('approval_step must be a list of persons, person ids'
                                    ', or person emails')
                self.approvals_rerequested.append([])
                for person in approval_step:
                    if isinstance(person, entities.Person):
                        self.approvals_rerequested[idx].append(person)
                    elif isinstance(person, int):
                        self.approvals_rerequested[idx].append(entities.Person(id=person))
                    else:
                        self.approvals_rerequested[idx].append(entities.Person(email=person))
        if subscribers_added:
            if not isinstance(subscribers_added, list):
                raise TypeError('subscribers_added must be a list')
            self.subscribers_added = []
            for person in subscribers_added:
                if isinstance(person, entities.Person):
                    self.subscribers_added.append(person)
                elif isinstance(person, int):
                    self.subscribers_added.append(entities.Person(id=person))
                else:
                    self.subscribers_added.append(entities.Person(email=person))
        if subscribers_removed:
            if not isinstance(subscribers_removed, list):
                raise TypeError('subscribers_removed must be a list')
            self.subscribers_removed = []
            for person in subscribers_removed:
                if isinstance(person, entities.Person):
                    self.subscribers_removed.append(person)
                elif isinstance(person, int):
                    self.subscribers_removed.append(entities.Person(id=person))
                else:
                    self.subscribers_removed.append(entities.Person(email=person))
        if subscribers_rerequested:
            if not isinstance(subscribers_rerequested, list):
                raise TypeError('subscribers_rerequested must be a list')
            self.subscribers_rerequested = []
            for person in subscribers_rerequested:
                if isinstance(person, entities.Person):
                    self.subscribers_rerequested.append(person)
                elif isinstance(person, int):
                    self.subscribers_rerequested.append(entities.Person(id=person))
                else:
                    self.subscribers_rerequested.append(entities.Person(email=person))
        if participants_added:
            if not isinstance(participants_added, list):
                raise TypeError('participants_added must be a list')
            self.participants_added = []
            for person in participants_added:
                try:
                    int(person)
                    self.participants_added.append(entities.Person(id=person))
                except ValueError:
                    self.participants_added.append(entities.Person(email=person))
        if participants_removed:
            if not isinstance(participants_removed, list):
                raise TypeError('participants_removed must be a list')
            self.participants_removed = []
            for person in participants_removed:
                try:
                    int(person)
                    self.participants_removed.append(entities.Person(id=person))
                except ValueError:
                    self.participants_removed.append(entities.Person(email=person))
        if field_updates:
            self.field_updates = []
            for field_update in field_updates:
                if isinstance(field_update, entities.FormField):
                    self.field_updates.append(field_update)
                else:
                    if 'name' not in field_update and 'id' not in field_update:
                        raise TypeError('each field_update in field_updates '
                                        'must contain field id or name')
                    if 'value' not in field_update:
                        raise TypeError('each field_update in field_updates must '
                                        'contain field value')
                    self.field_updates.append(field_update)
        if due_date:
            if not isinstance(due_date, datetime):
                raise TypeError('due_date must be a date')
            self.due_date = datetime.strftime(due_date, constants.DATE_FORMAT)
        if due:
            if not isinstance(due, datetime):
                raise TypeError('due must be a date')
            self.due = datetime.strftime(due, constants.DATE_TIME_FORMAT)
        if duration:
            if not isinstance(due, int):
                raise TypeError('duration must be an int')
            if not due:
                raise ValueError("duration can only be used with due")
            self.duration = duration
        if scheduled_date:
            if not isinstance(scheduled_date, datetime):
                raise TypeError('scheduled_date must be a date')
            self.scheduled_date = datetime.strftime(scheduled_date, constants.DATE_FORMAT)
            if hasattr(self, 'scheduled_datetime_utc'):
                delattr(self, 'scheduled_datetime_utc')
            if hasattr(self, 'cancel_schedule'):
                delattr(self, 'cancel_schedule')
        if cancel_schedule:
            if not isinstance(cancel_schedule, bool):
                raise TypeError('cancel_schedule must be a bool')
            self.cancel_schedule = cancel_schedule
            if hasattr(self, 'scheduled_datetime_utc'):
                delattr(self, 'scheduled_datetime_utc')
            if hasattr(self, 'scheduled_date'):
                delattr(self, 'scheduled_date')
        if scheduled_datetime_utc:
            if not isinstance(scheduled_datetime_utc, datetime):
                raise TypeError('scheduled_datetime_utc must be a date')
            self.scheduled_datetime_utc = datetime.strftime(scheduled_datetime_utc, constants.DATE_TIME_FORMAT)
            if hasattr(self, 'scheduled_date'):
                delattr(self, 'scheduled_date')
            if hasattr(self, 'cancel_schedule'):
                delattr(self, 'cancel_schedule')
        if added_list_ids:
            if not isinstance(added_list_ids, list):
                raise TypeError('added_list_ids must be a list of int')
            for item in added_list_ids:
                if not isinstance(item, int):
                    raise TypeError('added_list_ids must be a list of int')
            self.added_list_ids = added_list_ids
        if removed_list_ids:
            if not isinstance(removed_list_ids, list):
                raise TypeError('removed_list_ids must be a list of int')
            for item in removed_list_ids:
                if not isinstance(item, int):
                    raise TypeError('removed_list_ids must be a list of int')
            self.removed_list_ids = removed_list_ids
        if approval_steps:
            if not isinstance(approval_steps, list):
                raise TypeError('approval_steps must be a list of int')
            for item in approval_steps:
                if not isinstance(item, int):
                    raise TypeError('approval_steps must be a list of int')
            self.approval_steps = approval_steps
        if due and due_date:
            raise ValueError("either due_date or due can be set")
        if channel:
            if not isinstance(channel, str):
                raise TypeError('channel must be an instance of str')
            if channel not in ['email', 'telegram', 'web', 'facebook', 'vk', 'viber', 'mobile_app', 'web_widget',
                               'moy_sklad', 'zadarma', 'amo_crm', 'instagram']:
                raise TypeError('channel must be correct')
            self.channel = entities.Channel(type=channel)
        if spent_minutes:
            if not isinstance(spent_minutes, int):
                raise TypeError('spent_minutes must be an int')
            self.spent_minutes = spent_minutes


class CreateTaskRequest(object):
    """
        CreateTaskRequest
        
        Args:
            parent_task_id (:obj:`int`, optional): Parent task id
            attachments (:obj:`list` of :obj:`str` or :obj:`models.entities.NewFile`, optional): List of files to attach to the task
            list_ids (:obj:`list` of :obj:`int`, optional): List of list identifiers to which you want to add the task
            scheduled_date (:obj:`datetime`, optional): task scheduled date
            scheduled_datetime_utc (:obj:`datetime`, optional): task scheduled date with utc time
            subscribers (:obj:`list` of :obj:`models.entities.Person`, optional): List of task subscribers
        Args(Simple task):
            text (:obj:`str`): Task text. Required for a simple task
            subject (:obj:`str`, optional): Task subject
            due (:obj:`datetime`, optional): task due date with time (either due_date or due can be used)
            due_date (:obj:`datetime`, optional): task due date (either due_date or due can be used)
            duration (:obj:`int`, optional): duration of the event in minutes (it can only be used with due)
            responsible (:obj:`models.entities.Person`, optional): Responsible for the task
            participants (:obj:`list` of :obj:`models.entities.Person`, optional): List of task participants
        Args(Form task):
            form_id (:obj:`int`) Form template id. Required for a form task
            fields (:obj:`list` of :obj:`models.entities.FormField`, optional): List of field values
            approvals (:obj:`list` of :obj:`list` of :obj:`models.entities.Person`, optional) List of approval steps to add to the task
            fill_defaults (:obj:`bool`, optional): Flag indicating that task should be created with default values from the form template
    """

    def __init__(self, text=None, subject=None, parent_task_id=None,
                 due_date=None, form_id=None, attachments=None, responsible=None,
                 fields=None, approvals=None, subscribers=None, participants=None, list_ids=None,
                 due=None, duration=None, scheduled_date=None, scheduled_datetime_utc=None,
                 fill_defaults=None):
        if text:
            self.text = text
        if subject:
            self.subject = subject
        if parent_task_id:
            if not isinstance(parent_task_id, int):
                raise TypeError('parent_task_id must be an int')
            self.parent_task_id = parent_task_id
        if due_date:
            if not isinstance(due_date, datetime):
                raise TypeError('due_date must be a date')
            self.due_date = datetime.strftime(due_date, constants.DATE_FORMAT)
        if due:
            if not isinstance(due, datetime):
                raise TypeError('due must be a date')
            self.due = datetime.strftime(due, constants.DATE_TIME_FORMAT)
        if duration:
            if not isinstance(duration, int):
                raise TypeError('duration must be an int')
            self.duration = duration
        if scheduled_date:
            if not isinstance(scheduled_date, datetime):
                raise TypeError('scheduled_date must be a date')
            self.scheduled_date = datetime.strftime(scheduled_date, constants.DATE_FORMAT)
            if hasattr(self, 'scheduled_datetime_utc'):
                delattr(self, 'scheduled_datetime_utc')
        if scheduled_datetime_utc:
            if not isinstance(scheduled_datetime_utc, datetime):
                raise TypeError('scheduled_datetime_utc must be a date')
            self.scheduled_datetime_utc = datetime.strftime(scheduled_datetime_utc, constants.DATE_TIME_FORMAT)
            if hasattr(self, 'scheduled_date'):
                delattr(self, 'scheduled_date')
        if form_id:
            if not isinstance(form_id, int):
                raise TypeError('form_id must be int')
            self.form_id = form_id
        if attachments:
            if not isinstance(attachments, list):
                raise TypeError('attachments must be a list')
            self.attachments = []
            for attachment in attachments:
                self.attachments.append(attachment)
        if responsible:
            if isinstance(responsible, entities.Person):
                self.responsible = responsible
            elif isinstance(responsible, int):
                self.responsible = entities.Person(id=responsible)
            else:
                self.responsible = entities.Person(email=responsible)
        if fields:
            self.fields = []
            for field in fields:
                if isinstance(field, entities.FormField):
                    self.fields.append(field)
                else:
                    if 'name' not in field and 'id' not in field:
                        raise TypeError('each field in fields '
                                        'must contain field id or name')
                    if 'value' not in field:
                        raise TypeError('each field in fields must '
                                        'contain field value')
                    self.fields.append(field)
        if approvals:
            if not isinstance(approvals, list):
                raise TypeError('approvals must be a list')
            self.approvals = []
            for idx, approval_step in enumerate(approvals):
                if not isinstance(approval_step, list):
                    raise TypeError('approval_step must be a list of persons, person ids'
                                    ', or person emails')
                self.approvals.append([])
                for person in approval_step:
                    if isinstance(person, entities.Person):
                        self.approvals[idx].append(person)
                    elif isinstance(person, int):
                        self.approvals[idx].append(entities.Person(id=person))
                    else:
                        self.approvals[idx].append(entities.Person(email=person))
        if subscribers:
            if not isinstance(subscribers, list):
                raise TypeError('subscribers must be a list')
            self.subscribers = []
            for person in subscribers:
                if isinstance(person, entities.Person):
                    self.subscribers.append(person)
                elif isinstance(person, int):
                    self.subscribers.append(entities.Person(id=person))
                else:
                    self.subscribers.append(entities.Person(email=person))
        if participants:
            if not isinstance(participants, list):
                raise TypeError('participants must be a list')
            self.participants = []
            for person in participants:
                try:
                    int(person)
                    self.participants.append(entities.Person(id=person))
                except ValueError:
                    self.participants.append(entities.Person(email=person))
        if list_ids:
            if not isinstance(list_ids, list):
                raise TypeError('list_ids must be a list of int')
            for item in list_ids:
                if not isinstance(item, int):
                    raise TypeError('list_ids must be a list of int')
            self.list_ids = list_ids
        if fill_defaults:
            if not isinstance(fill_defaults, bool):
                raise TypeError("fill_defaults must be a boolean")
            self.fill_defaults = fill_defaults


class AuthRequest(object):
    """
        AuthRequest

        Args:
            login (:obj:`str`): User's login (email)
            security_key (:obj:`str`): User's secret key
    """

    def __init__(self, login, security_key):

        if login:
            self.login = login
        if security_key:
            self.security_key = security_key


class SyncCatalogRequest(object):
    """
        SyncCatalogRequest
        
        Args:
            catalog_headers (:obj:`list` of :obj:`str` or :obj:`models.entities.CatalogHeader`): List of new catalog headers
            items (:obj:`list` of :obj:`models.entities.CatalogItem`, optional): List of new catalog items
            apply (:obj:`bool`, optional): Flag indicates if changes must be applied. By default false
    """

    def __init__(self, apply=None, catalog_headers=None, items=None):
        if apply:
            if not isinstance(apply, bool):
                raise TypeError('apply must be a bool')
            self.apply = apply
        if catalog_headers:
            self.catalog_headers = _get_catalog_headers(catalog_headers)
        if items:
            self.items = _get_catalog_items(items)


class CreateCatalogRequest(object):
    """
        CreateCatalogRequest
        
        Args:
            name (:obj:`str`): Catalog name
            catalog_headers (:obj:`list` of :obj:`str`): List of catalog headers
            items (:obj:`list` of :obj:`models.entities.str` or :obj:`models.entities.CatalogHeader`, optional): List of catalog items
    """

    def __init__(self, name=None, catalog_headers=None, items=None):
        if name:
            if not isinstance(name, str):
                raise TypeError('name must be a str')
            self.name = name
        if catalog_headers:
            self.catalog_headers = _get_catalog_headers(catalog_headers)
        if items:
            self.items = _get_catalog_items(items)


def _get_catalog_headers(catalog_headers):
    if not isinstance(catalog_headers, list):
        raise TypeError('catalog_headers must be a list of str')

    headers = []
    for item in catalog_headers:
        if isinstance(item, entities.CatalogHeader):
            headers.append(item.name)
        elif isinstance(item, str):
            headers.append(item)
        else:
            raise TypeError('list_ids must be a list of str or models.entities.CatalogHeader')
    return headers


def _get_catalog_items(catalog_items):
    if not isinstance(catalog_items, list):
        raise TypeError('catalog_items must be a list')

    items = []
    for item in catalog_items:
        try:
            items.append(entities.CatalogItem.fromliststr(item))
        except TypeError:
            if not isinstance(item, entities.CatalogItem):
                raise TypeError('catalog_items must be a list of str or models.entities.CatalogItems')
            items.append(item)
    return items


def _date_to_str(str_date, property_name):
    if not isinstance(str_date, datetime):
        raise TypeError('{} must be a date'.format(property_name))
    return datetime.strftime(str_date, constants.DATE_TIME_FORMAT)

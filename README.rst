==============================
pyrus-api
==============================
A python 3 client for the Pyrus API.

The full documentation for API can be found here_.

.. _here: https://pyrus.com/en/help/api/

-----------------
Installation
-----------------

To get the latest version:
  - pip_ (preffrered)
      $ pip install --upgrade pyrus-api
  - Setuptools_: Use the easy_install tool included in the setuptools package:
      $ easy_install --upgrade pyrus-api
  - Manual installation: `Download the latest version of pyrus-api client`_, unpack the code, and run 
      $ python setup.py install

.. _pip: https://pypi.python.org/pypi/pip
.. _Setuptools: https://pypi.python.org/pypi/setuptools
.. _`Download the latest version of pyrus-api client`: https://pypi.python.org/pypi/pyrus-api/

-----------------
Usage
-----------------
To start with the module:
    
    >>>  from pyrus import client
    >>>  import pyrus.models
    >>>  pyrus_client = client.PyrusAPI(login='login@pyrus.com', security_key='sadf2R5Wrdkn..')

-----------------
Examples
-----------------
Authenticate:
    
    >>> pyrus_client.auth()

Get all form templates:

    >>> forms_response = pyrus_client.get_forms()
    >>> forms = forms_response.forms

Get list of tasks created using specified form:

    >>> form_register_response = pyrus_client.get_registry(forms[0].id)
    >>> tasks = form_register_response.tasks

You can also filter registry by specific field value, status or current step number:

    >>> request = pyrus.models.requests.FormRegisterRequest(
            include_archive=True,
            steps=[1,2],
            filters=[pyrus.models.entities.EqualsFilter(1, "hello world")])
    >>> form_register_response = pyrus_client.get_registry(forms[0].id, request)

Get task with all comments:

    >>> task = pyrus_client.get_task(tasks[0].id).task

Add new comment to the task:

    >>> request = pyrus.models.requests.TaskCommentRequest(text="hello", action="finished")
    >>> task = pyrus_client.comment_task(tasks[0].id, request).task

Upload a file:
    >>> response = myclient.upload_file('C:\\path\\to\\file.txt').guid

Create a task:

    >>> request = CreateTaskRequest(
            text="Task from python client", 
            participants=['colleague@email.com', 10196] #you can specify person id, email, or pyrus.models.entities.Person object
            attachments = [guid])
    >>> task = pyrus_client.create_task(request).task

Get all available contacts:
    
    >>> contacts = pyrus_client.get_contacts()

Get catalog with all items:
    
    >>> catalog_id = 1525
    >>> catalog_response = pyrus_client.get_catalog(catalog_id)
    >>> items = catalog_response.items
	
Get profile:

    >>> profile_response = pyrus_client.get_profile()

Get inbox:

    >>> inbox_response = pyrus_client.get_inbox(tasks_count=100)
    
Get calendar:

    >>> calendar_response = (pyrus_client.get_calendar_tasks(req.CalendarRequest(
	        datetime.datetime.utcnow() - datetime.timedelta(days=30),
	        datetime.datetime.utcnow() + datetime.timedelta(days=30),
	        all_accessed_tasks=True,
	        item_count=55,
	        filter_mask=0b0111)))

Get announcement with all comments:

    >>> announcement = pyrus_client.get_announcement(12321321).announcement
    
Get announcements with all comments:

    >>> announcements = pyrus_client.get_announcements().announcements

Add new comment to the announcement:

    >>> request = pyrus.models.requests.AnnouncementCommentRequest(text="hello", attachments = ['BEFCE22E-AEFF-4771-83D4-2A4B78FB05C6'])
    >>> announcement = pyrus_client.comment_announcement(12321321, request).announcement

Create an announcement:

    >>> request = CreateAnnouncementRequest(
            text="Announcement from python client", 
            attachments = [guid])
    >>> announcement = pyrus_client.create_announcement(request).announcement

Get form permissions:

    >>> permissions = pyrus_client.get_permissions(123)

Change form permissions:

    >>> request = pyrus.models.requests.ChangePermissionsRequest({1733:'member'})
    >>> changed_permissions = pyrus_client.change_permissions(123, request)

-----------------
Support
-----------------
If you have any questions or comments please send an email to support@pyrus.com

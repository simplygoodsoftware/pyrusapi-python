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

  $ pip install pyrus-api

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

-----------------
Support
-----------------
If you have any questions or comments please send an email to support@pyrus.com

# pyrus-api

[![PyPI version](https://badge.fury.io/py/pyrus-api.svg)](https://badge.fury.io/py/pyrus-api)

A Python 3 client for the Pyrus API.
The full documentation for API can be found [here](https://pyrus.com/en/help/api/)

## Getting Started

* instal pyrus-api library:
    * [pip](https://pypi.python.org/pypi/pip) (preffered)

        ````
        $ pip install --upgrade pyrus-api
        ````
    * [Setuptools](https://pypi.python.org/pypi/setuptools): Use the easy_install tool included in the setuptools package:

        ````
        $ easy_install --upgrade pyrus-api
        ````
    * Manual installation: [Download the latest version of pyrus-api client](https://pypi.python.org/pypi/pyrus-api/), unpack the code, and run:

        ````
        $ python setup.py install
        ````

* Import packages into your project:

```python   
from pyrus import client
import pyrus.models
```
* Create API client:

```python
pyrus_client = client.PyrusAPI(login='login@pyrus.com', security_key='sadf2R5Wrdkn..')
```

* Perform authorization:

```python
auth_response = pyrus_client.auth()
if auth_response.success:
    pass
```

## Forms

* Get all form templates:

```python
forms_response = pyrus_client.get_forms()
forms = forms_response.forms
```

* Get tasks list by form template:

```python
request = pyrus.models.requests.FormRegisterRequest(
        include_archived=True,
        steps=[1,2],
        filters=[pyrus.models.entities.EqualsFilter(1, "hello world")])
form_register_response = pyrus_client.get_registry(forms[0].id, request)
tasks = form_register_response.tasks
```

## Tasks

* Get task with all comments:

```python
task = pyrus_client.get_task(tasks[0].id).task
```

* Add task comment:

```python
request = pyrus.models.requests.TaskCommentRequest(text="hello", action="finished")
task = pyrus_client.comment_task(tasks[0].id, request).task
```

* Create a task:

```python
request = CreateTaskRequest(
        text="Task from python client", 
        participants=['colleague@email.com', 10196]
        attachments = ['BEFCE22E-AEFF-4771-83D4-2A4B78FB05C6'])
task = pyrus_client.create_task(request).task
```

## Files

* Upload a file:

```python
response = pyrus_client.upload_file('C:\\path\\to\\file.txt').guid
```

## Catalogs

* Get catalog with all items:
    
```python
catalog_id = 1525
catalog_response = pyrus_client.get_catalog(catalog_id)
items = catalog_response.items
```

* Create catalog

```python
request = pyrus.models.requests.CreateCatalogRequest(
        name = "NewCatalog",
        catalog_headers = ["Column1", "Column2", "Column3"],
        items = [
            ["A1", "A2", "A3"],
            ["B1", "B2", "B3"],
            ["C1", "C2", "C3"]
        ]
    )
catalog_id = pyrus_client.create_catalog(request).catalog_id
```

* Sync catalog (All unspecified catalog items and text columns will be deleted)

```python
catalog_id = 7825
request = pyrus.models.requests.SyncCatalogRequest(
        apply = True,
        catalog_headers = ["Column1", "Column4", "Column3"],
        items = [
            ["A1", "A2", "A3"],
            ["B1", "B4", "B5"],
            ["D1", "D2", "D3"]
        ]
    )
response = pyrus_client.sync_catalog(catalog_id, request)
deleted = response.deleted
updated = response.updated
added = response.added
new_headers = response.catalog_headers
```

* Change catalog items

```python
catalog_id = 7825
request = pyrus.models.requests.UpdateCatalogItemsRequest(
        upsert = [
            ["A1", "A5", "A6"],
            ["E1", "E2", "E3"]
        ],
        delete = ["B1"]
    )
response = pyrus_client.update_catalog_items(catalog_id, request)
deleted = response.deleted
updated = response.updated
added = response.added
```

## Contacts

* Get all available contacts:

```python    
contacts = pyrus_client.get_contacts()
```

## Lists

* Get all lists

```python
response = pyrus_client.get_lists()
lists = response.lists
```

* Get all tasks in list

```python
list_id = 1522
response = pyrus_client.get_task_list(list_id, item_count=25, include_archived=True)
tasks = response.tasks
```

## Profile

* Get profile:

```python
profile_response = pyrus_client.get_profile()
```

## Roles

* Get all organization roles:

```python
roles_response = pyrus_client.get_roles()
roles = roles_response.roles
```

* Create role:

```python
create_role_request = CreateRoleRequest(
            name='TechSupport',
            members=[1233, 3043])
role_response = pyrus_client.create_role(create_role_request)
```

* Update role:
    
```python
Update_role_request = UpdateRoleRequest(
            name='InternalTechSupport',
            added_members=[2766],
            removed_members=[1233])
role_response = pyrus_client.update_role(create_role_request)
```

## Profile

* Get profile:

```python
profile_response = pyrus_client.get_profile()
```

## Inbox

* Get inbox:

```python
inbox_response = pyrus_client.get_inbox(tasks_count=100)
```
## Calendar

* Get calendar:

```python
calendar_response = (pyrus_client.get_calendar_tasks(req.CalendarRequest(
	datetime.datetime.utcnow() - datetime.timedelta(days=30),
	datetime.datetime.utcnow() + datetime.timedelta(days=30),
	all_accessed_tasks=True,
	item_count=55,
	filter_mask=0b0111)))
```

## Announcements

* Get announcement with all comments:

```python
announcement = pyrus_client.get_announcement(12321321).announcement
```

* Get announcements with all comments:

```python
announcements = pyrus_client.get_announcements().announcements
```

* Add announcement comment:

```python
request = pyrus.models.requests.AnnouncementCommentRequest(text="hello", attachments = ['BEFCE22E-AEFF-4771-83D4-2A4B78FB05C6'])
announcement = pyrus_client.comment_announcement(12321321, request).announcement
```

* Create an announcement:

```python
request = CreateAnnouncementRequest(
        text="Announcement from python client", 
        attachments = ['BEFCE22E-AEFF-4771-83D4-2A4B78FB05C6'])
announcement = pyrus_client.create_announcement(request).announcement
```

## Form permissions

* Get form permissions:

```python
permissions = pyrus_client.get_permissions(123)
```

* Change form permissions:

```python
request = pyrus.models.requests.ChangePermissionsRequest({1733:'member'})
changed_permissions = pyrus_client.change_permissions(123, request)
```

## Support

If you have any questions or comments please send an email to support@pyrus.com

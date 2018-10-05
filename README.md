# pyrus-api

[![PyPI version](https://badge.fury.io/py/pyrus-api.svg)](https://badge.fury.io/py/pyrus-api)

A Python 3 client for the Pyrus API.

## Getting Started

* instal pyrus-api library using pip:

````
$ pip install pyrus-api
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
```

## Forms

* Get all form templates:

```python
forms_response = pyrus_client.forms()
forms = forms_response.forms
```

* Get tasks list by form template:

```python
request = pyrus.models.requests.FormRegisterRequest(
        include_archive=True,
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
delted = response.deleted
updated = response.updated
added = response.added
new_headers = response.catalog_headers
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

## Support

If you have any questions or comments please send an email to support@pyrus.com

'''
PyrusAPI library

This module allows you to call Pyrus API methods via python.
usage:

    >>> from pyrus import client
    >>> import pyrus.models
    >>> pyrus_client = client.PyrusAPI()
    >>> auth_response = pyrus_client.auth("login", "security_key")
    >>> if auth_response.success:
           forms_response = pyrus_client.get_forms()
           forms = forms_response.forms

Full documentation for PyrusAPI is at https://pyrus.com/en/help/api
'''

from enum import Enum
import jsonpickle
import os
import re
import requests
from .models import responses as resp, requests as req, entities as ent
import cgi


class PyrusAPI(object):
    """
    PyrusApi client

    Args:
        login (:obj:`str`): User's login (email)
        security_key (:obj:`str`): User's Secret key
        access_token (:obj:`str`, optional): Users's access token. You can specify it if you already have one. (optional)
        proxy (:obj:`str`, optional): Proxy server url
    """
    MAX_FILE_SIZE_IN_BYTES = 250 * 1024 * 1024

    class HTTPMethod(Enum):
        GET = "GET"
        POST = "POST"
        PUT = "PUT"

    _host = 'api.pyrus.com'
    _base_path = '/v4'
    access_token = None
    _protocol = 'https'
    _api_name = 'Pyrus'
    _user_agent = 'Pyrus API python client v 2.22.0'
    proxy = None
    _download_file_base_url = 'https://files.pyrus.com/services/attachment?Id='

    def __init__(self, login=None, security_key=None, access_token=None, proxy=None):
        self.security_key = security_key
        self.access_token = access_token
        self.login = login
        if proxy:
            self.proxy = {'http': proxy}

    def auth(self, login=None, security_key=None):
        """
        Get access_token for user

        Args:
            login (:obj:`str`): User's login (email)
            security_key (:obj:`str`): User's Secret key

        Returns: 
            class:`models.responses.AuthResponse` object
        """
        if login:
            self.login = login
        if security_key:
            self.security_key = security_key
        response = self._auth()
        return resp.AuthResponse(**response)

    def get_forms(self):
        """
        Get all available form templates

        Returns: 
            class:`models.responses.FormsResponse` object
        """
        url = self._create_url('/forms')
        response = self._perform_get_request(url)
        return resp.FormsResponse(**response)

    def get_registry(self, form_id, form_register_request=None):
        """
        Get a list of tasks based on the form template

        Args:
            form_id (:obj:`int`): Form id
            form_register_request (:obj:`models.requests.FormRegisterRequest`, optional): Request filters.

        Returns: 
            class:`models.responses.FormRegisterResponse` object
        """
        url = self._create_url('/forms/{}/register'.format(form_id))
        if form_register_request:
            if not isinstance(form_register_request, req.FormRegisterRequest):
                raise TypeError('form_register_request must be an instance '
                                'of models.requests.FormRegisterRequest')
            response = self._perform_post_request(url, form_register_request)
        else:
            response = self._perform_get_request(url)

        if form_register_request and getattr(form_register_request, 'format', 'json') == "csv":
            return response

        return resp.FormRegisterResponse(**response)

    def get_contacts(self, include_inactive = False):
        """
        Get a list of contacts available to the current user and grouped by organization

        Args:
            include_inactive (:obj:`bool`, optional):  Should inactive persons be included to the response

        Returns: 
            class:`models.responses.ContactsResponse` object
        """
        url = self._create_url('/contacts?include_inactive={}'.format(include_inactive))
        response = self._perform_get_request(url)
        return resp.ContactsResponse(**response)

    def get_catalog(self, catalog_id):
        """
        Get a catalog

        Args:
            catalog_id (:obj:`int`): Catalog id

        Returns: 
            class:`models.responses.CatalogResponse` object
        """
        if not isinstance(catalog_id, int):
            raise Exception("catalog_id should be valid int")

        url = self._create_url('/catalogs/{}'.format(catalog_id))
        response = self._perform_get_request(url)
        return resp.CatalogResponse(**response)

    def get_form(self, form_id):
        """
        Get the form template

        Args:
            form_id (:obj:`int`): form id

        Returns:
            class:`models.responses.FormResponse` object
        """
        if not isinstance(form_id, int):
            raise Exception("form_id should be valid int")

        url = self._create_url('/forms/{}'.format(form_id))
        response = self._perform_get_request(url)
        return resp.FormResponse(**response)

    def get_task(self, task_id):
        """
        Get the task

        Args:
            task_id (:obj:`int`): Task id

        Returns: 
            class:`models.responses.TaskResponse` object
        """
        if not isinstance(task_id, int):
            raise Exception("task_id should be valid int")
        url = self._create_url('/tasks/{}'.format(task_id))
        response = self._perform_get_request(url)
        return resp.TaskResponse(**response)
    
    def get_announcement(self, announcement_id):
        """
        Get the announcement

        Args:
            announcement_id (:obj:`int`): Announcement id

        Returns: 
            class:`models.responses.AnnouncementResponse` object
        """
        if not isinstance(announcement_id, int):
            raise Exception("announcement_id should be valid int")
        url = self._create_url('/announcements/{}'.format(announcement_id))
        response = self._perform_get_request(url)
        return resp.AnnouncementResponse(**response)

    def comment_task(self, task_id, task_comment_request):
        """
        Add task comment. This method returns a task with all comments, including the added one.
        Args:
            task_id (:obj:`int`): Task id
            task_comment_request (:obj:`models.requests.TaskCommentRequest`): Comment data.

        Returns:
            class:`models.responses.TaskResponse` object
        """
        if not isinstance(task_id, int):
            raise Exception("task_id should be valid int")
        url = self._create_url('/tasks/{}/comments'.format(task_id))
        if not isinstance(task_comment_request, req.TaskCommentRequest):
            raise TypeError('form_register_request must be an instance '
                            'of models.requests.TaskCommentRequest')
        response = self._perform_post_request(url, task_comment_request)
        return resp.TaskResponse(**response)
    
    def comment_announcement(self, announcement_id, announcement_comment_request):
        """
        Add announcement comment. This method returns the announcement with all comments.
        Args:
            announcement_id (:obj:`int`): Announcement id
            announcement_comment_request (:obj:`models.requests.AnnouncementCommentRequest`): Comment data.

        Returns:
            class:`models.responses.AnnouncementResponse` object
        """
        if not isinstance(announcement_id, int):
            raise Exception("announcement_id should be valid int")
        url = self._create_url('/announcements/{}/comments'.format(announcement_id))
        if not isinstance(announcement_comment_request, req.AnnouncementCommentRequest):
            raise TypeError('announcement_comment_request must be an instance '
                            'of models.requests.AnnouncementCommentRequest')
        response = self._perform_post_request(url, announcement_comment_request)
        return resp.AnnouncementResponse(**response)

    def create_task(self, create_task_request):
        """
        Create task. This method returns a created task with a comment.

        Args:
            task_comment_request (:obj:`models.requests.CreateTaskRequest`)

        Returns: 
            class:`models.responses.TaskResponse` object
        """
        url = self._create_url('/tasks')
        if not isinstance(create_task_request, req.CreateTaskRequest):
            raise TypeError('create_task_request must be an instance '
                            'of models.requests.CreateTaskRequest')
        response = self._perform_post_request(url, create_task_request)
        return resp.TaskResponse(**response)

    def get_announcements(self):
        """
        Get all announcements.


        Returns: 
            class:`models.responses.AnnouncementsResponse` object
        """
        url = self._create_url('/announcements')
        response = self._perform_get_request(url)

        return resp.AnnouncementsResponse(**response)
    def create_announcement(self, create_announcement_request):
        """
        Create announcement. This method returns the created announcement.

        Args:
            task_announcement_request (:obj:`models.requests.CreateAnnouncementRequest`)

        Returns: 
            class:`models.responses.AnnouncementResponse` object
        """
        url = self._create_url('/announcements')
        if not isinstance(create_announcement_request, req.CreateAnnouncementRequest):
            raise TypeError('create_announcement_request must be an instance '
                            'of models.requests.CreateAnnouncementRequest')
        response = self._perform_post_request(url, create_announcement_request)
        return resp.AnnouncementResponse(**response)

    def upload_file(self, file_path):
        """
        Upload files for subsequent attachment to tasks.

        Args:
            file_path (:obj:`str`): Path to the file

        Returns: 
            class:`models.responses.UploadResponse` object
        """
        url = self._create_url('/files/upload')
        response = self._perform_request_with_retry(url, self.HTTPMethod.POST, file_path=file_path)
        return resp.UploadResponse(**response)

    def get_lists(self):
        """
        Get all the lists that are available to the user.

        Returns: 
            class:`models.responses.ListsResponse` object
        """
        url = self._create_url('/lists')
        response = self._perform_get_request(url)
        return resp.ListsResponse(**response)

    def get_task_list(self, list_id, item_count=200, include_archived=False):
        """
        Get all tasks in the list.

        Args:
            list_id (:obj:`int`): List id
            item_count (:obj:`int`, optional): The maximum number of tasks in the response, the default is 200
            include_archived (:obj:`bool`, optional): Should archived tasks be included to the response, the default is False

        Returns: 
            class:`models.responses.TaskListResponse` object
        """
        if not isinstance(list_id, int):
            raise TypeError('list_id must be an instance of int')
        if not isinstance(item_count, int):
            raise TypeError('item_count must be an instance of int')
        if not isinstance(include_archived, bool):
            raise TypeError('include_archived must be an instance of bool')

        url_suffix = '/lists/{}/tasks?item_count={}'.format(list_id, item_count)
        if include_archived:
            url_suffix += '&include_archived=y'

        url = self._create_url(url_suffix)
        response = self._perform_get_request(url)
        return resp.TaskListResponse(**response)
    
    def get_task_list(self, list_id, task_list_request=None):
        """
        Get all tasks in the list.

        Args:
            list_id (:obj:`int`): List id
            task_list_request (:obj:`models.requests.TaskListRequest`, optional): Request filters.

        Returns: 
            class:`models.responses.TaskListResponse` object
        """
        url = self._create_url('/lists/{}/tasks'.format(list_id))
        if task_list_request:
            if not isinstance(task_list_request, req.TaskListRequest):
                raise TypeError('task_list_request must be an instance '
                                'of models.requests.TaskListRequest')
            response = self._perform_post_request(url, task_list_request)
        else:
            response = self._perform_get_request(url)

        return resp.TaskListResponse(**response)

    def download_file(self, file_id):
        """
        Download the file.

        Args:
            file_id (:obj:`int`): File id

        Returns: 
            class:`models.responses.DownloadResponse` object
        """
        if not isinstance(file_id, int):
            raise TypeError('file_id must be an instance of int')
        url = self._download_file_base_url + str(file_id)
        response = self._perform_get_file_request(url)
        if response.status_code == 200:
            try:
                _ , params= cgi.parse_header(response.headers['Content-Disposition'])
                filename = params['filename']
            except:
                filename = re.findall('filename=(.+)', response.headers['Content-Disposition'])
            return resp.DownloadResponse(filename, response.content)
        else:
            if response.status_code == 401:
                return resp.BaseResponse(**{'error_code': 'authorization_error'})
            if response.status_code == 403 or response.status_code == 404:
                return resp.BaseResponse(**{'error_code': 'access_denied_file'})
            else:
                return resp.BaseResponse(**{'error_code': 'ServerError'})

    def create_catalog(self, create_catalog_request):
        """
        Create a catalog. This request returns created catalog with all elements

        Args:
            create_catalog_request (:obj:`models.requests.CreateCatalogRequest`): Catalog data.

        Returns: 
            class:`models.responses.CatalogResponse` object
        """
        url = self._create_url('/catalogs')
        if not isinstance(create_catalog_request, req.CreateCatalogRequest):
            raise TypeError('create_catalog_request must be an instance '
                            'of models.requests.CreateCatalogRequest')
        response = self._perform_put_request(url, create_catalog_request)
        return resp.CatalogResponse(**response)

    def sync_catalog(self, catalog_id, sync_catalog_request):
        """
        Sync a catalog. This method updates catalog headers and items. 
        You must define all the values and text columns that need to remain in the catalog.
        All unspecified items and text columns will be deleted.
        This method returns a list of items that have been added, modified, or deleted

        Args:
            sync_catalog_request (:obj:`models.requests.SyncCatalogRequest`): Catalog data.

        Returns: 
            class:`models.responses.SyncCatalogResponse` object
        """
        if not isinstance(catalog_id, int):
            raise TypeError("catalog_id must be an instance of int")
        url = self._create_url('/catalogs/{}'.format(catalog_id))
        if not isinstance(sync_catalog_request, req.SyncCatalogRequest):
            raise TypeError('sync_catalog_request must be an instance '
                            'of models.requests.SyncCatalogRequest')
        response = self._perform_post_request(url, sync_catalog_request)
        return resp.SyncCatalogResponse(**response)
        
    def get_roles(self):
        """
        Get all roles from user's organization
        Returns: 
            class:`models.responses.RolesResponse` object
        """

        url = self._create_url('/roles')
        response = self._perform_get_request(url)
        return resp.RolesResponse(**response)

    def get_role(self, role_id):
        """
        Get a role
        Args:
            role_id
        Returns:
            class:`models.responses.RoleResponse` object
        """

        url = self._create_url('/roles/{}'.format(role_id))
        response = self._perform_get_request(url)
        return resp.RoleResponse(**response)

    def create_role(self, create_role_request):
        """
        Creates a role
        Args:
            create_role_request (:obj:`models.requests.CreateRoleRequest`): Role data.
        Returns: 
            class:`models.responses.RoleResponse` object
        """

        url = self._create_url('/roles')
        if not isinstance(create_role_request, req.CreateRoleRequest):
            raise TypeError('create_role_request must be an instance '
                            'of models.requests.CreateRoleRequest')

        response = self._perform_post_request(url, create_role_request)
        return resp.RoleResponse(**response)

    def update_role(self, role_id, update_role_request):
        """
        Updates a role
        Args:
            role_id (:obj:`int`): Role id
            update_role_request (:obj:`models.requests.UpdateRoleRequest`): Role data.
        Returns: 
            class:`models.responses.RoleResponse` object
        """

        url = self._create_url('/roles/{}'.format(role_id))
        if not isinstance(update_role_request, req.UpdateRoleRequest):
            raise TypeError('update_role_request must be an instance '
                            'of models.requests.UpdateRoleRequest')

        response = self._perform_put_request(url, update_role_request)
        return resp.RoleResponse(**response)

    def get_members(self):
        """
        Get all members from user's organization
        Returns: 
            class:`models.responses.MembersResponse` object
        """

        url = self._create_url('/members')
        response = self._perform_get_request(url)
        return resp.MembersResponse(**response)

    def get_member(self, member_id):
        """
        Get a member
        Args:
            member_id
        Returns:
            class:`models.responses.MemberResponse` object
        """

        url = self._create_url('/members/{}'.format(member_id))
        response = self._perform_get_request(url)
        return resp.MemberResponse(**response)

    def create_member(self, create_member_request):
        """
        Creates a member
        Args:
            create_member_request (:obj:`models.requests.CreateMemberRequest`): Member data.
        Returns: 
            class:`models.responses.MemberResponse` object
        """

        url = self._create_url('/members')
        if not isinstance(create_member_request, req.CreateMemberRequest):
            raise TypeError('create_member_request must be an instance '
                            'of models.requests.CreateMemberRequest')

        response = self._perform_post_request(url, create_member_request)
        print("~~ create_member: ", response)
        return resp.MemberResponse(**response)

    def update_member(self, member_id, update_member_request):
        """
        Updates a member
        Args:
            member_id (:obj:`int`): Member id
            update_member_request (:obj:`models.requests.UpdateMemberRequest`): Member data.
        Returns: 
            class:`models.responses.MemberResponse` object
        """

        url = self._create_url('/members/{}'.format(member_id))
        if not isinstance(update_member_request, req.UpdateMemberRequest):
            raise TypeError('update_member_request must be an instance '
                            'of models.requests.UpdateMemberRequest')

        response = self._perform_put_request(url, update_member_request)
        return resp.MemberResponse(**response)

    def set_avatar(self, member_id, file_guid, external_avatar_id=None):
        """
        Sets a new avatar
        Args:
            member_id (:obj:`int`): Member id
            file_guid (:obj:`str`): A file GUID got from the file upload request.
            external_avatar_id (:obj:`int`): External avatar id
        Returns: 
            class:`models.responses.MemberResponse` object
        """

        url = self._create_url('/members/{}/avatar'.format(member_id))
        set_avatar_request = req.SetAvatarRequest(file_guid, external_avatar_id)
        response = self._perform_put_request(url, set_avatar_request)
        return resp.MemberResponse(**response)

    def get_profile(self, include_inactive = False):
        """
        Get a profile
        
        Args:
            include_inactive (:obj:`bool`, optional):  Should inactive persons be included to the response
        
        Returns: 
            class:`models.responses.ProfileResponse` object
        """

        url = self._create_url('/profile?withinactive={}'.format(include_inactive))
        response = self._perform_get_request(url)
        return resp.ProfileResponse(**response)

    def get_inbox(self, tasks_count=50):
        """
        Get inbox tasks

        Args:
            tasks_count (:obj:`int`, optional): The maximum number of tasks in the response, the default is 50

        Returns: 
            class:`models.responses.TaskListResponse` object
        """

        url = self._create_url('/inbox?item_count={}'.format(tasks_count))
        response = self._perform_get_request(url)
        return resp.TaskListResponse(**response)

    def get_calendar_tasks(self, calendar_request):
        """
        Get a calendar tasks. This method returns tasks from calendar for time interval
        Tasks can be with form or without. Response returns only last comment for all task

        Args:
            calendar_request: (:obj:`models.requests.CalendarRequest`): Calendar request data.

        Returns:
            class:`models.responses.CalendarResponse` object
        """
        if not isinstance(calendar_request, req.CalendarRequest):
            raise TypeError('calendar_request must be an instance '
                            'of models.requests.CalendarRequest')
        query = ('/calendar?'
                 'start_date_utc={}'
                 '&end_date_utc={}'
                 '&item_count={}'
                 '&all_accessed_tasks={}'
                 '&filter_mask={}').format(
            calendar_request.start_date_utc_str,
            calendar_request.end_date_utc_str,
            calendar_request.item_count, calendar_request.all_accessed_tasks,
            calendar_request.filter_mask
        )

        url = self._create_url(query)
        response = self._perform_get_request(url)
        return resp.CalendarResponse(**response)

    def serialize_request(self, body):
        return jsonpickle.encode(body, unpicklable=False).encode('utf-8')

    def get_form_permissions(self, form_id):
        """
        Get form permissions

        Args:
            form_id (:obj:`int`): Form id

        Returns: 
            class:`models.responses.PermissionsResponse` object
        """

        url = self._create_url('/forms/{}/permissions'.format(form_id))
        response = self._perform_get_request(url)
        return resp.PermissionsResponse(**response)

    def change_form_permissions(self, form_id, request):
        """
        Change form permissions

        Args:
            form_id (:obj:`int`): Form id

        Returns: 
            class:`models.responses.PermissionsResponse` object
        """

        if not isinstance(request, req.ChangePermissionsRequest):
            raise TypeError('request must be an instance of models.requests.ChangePermissionsRequest')

        url = self._create_url('/forms/{}/permissions'.format(form_id))
        response = self._perform_post_request(url, request)
        return resp.PermissionsResponse(**response)

    def _auth(self):
        url = self._create_url('/auth')
        headers = {
            'User-Agent': '{}'.format(self._user_agent),
            'Content-Type': 'application/json'
        }
        auth_request = req.AuthRequest(login=self.login, security_key=self.security_key)

        data = self.serialize_request(auth_request)

        auth_response = requests.post(url, headers=headers, data=data)
        # pylint: disable=no-member
        if auth_response.status_code == requests.codes.ok:
            response = auth_response.json()
            self.access_token = response['access_token']
        else:
            response = auth_response.json()
            self.access_token = None

        return response

    def _create_url(self, url):
        return '{}://{}{}{}'.format(self._protocol, self._host, self._base_path, url)

    def _perform_get_request(self, url):
        return self._perform_request_with_retry(url, self.HTTPMethod.GET)

    def _perform_get_file_request(self, url):
        return self._perform_request_with_retry(url, self.HTTPMethod.GET, get_file=True)

    def _perform_post_request(self, url, body=None):
        return self._perform_request_with_retry(url, self.HTTPMethod.POST, body)

    def _perform_put_request(self, url, body=None):
        return self._perform_request_with_retry(url, self.HTTPMethod.PUT, body)

    def _perform_request_with_retry(self, url, method, body=None, file_path=None, get_file=False):
        if not isinstance(method, self.HTTPMethod):
            raise TypeError('method must be an instanse of HTTPMethod Enum.')

        # try auth if no access token
        if not self.access_token:
            response = self._auth()
            if not self.access_token:
                return response

        # try to call api method
        response = self._perform_request(url, method, body, file_path, get_file)
        # if 401 try auth and call method again
        if response.status_code == 401:
            response = self._auth()
            # if failed return auth response
            if not self.access_token:
                return response

            response = self._perform_request(url, method, body, file_path, get_file)

        return self._get_response(response, get_file, body)

    def _perform_request(self, url, method, body, file_path, get_file):
        if method == self.HTTPMethod.POST:
            if file_path:
                return self._post_file_request(url, file_path)
            return self._post_request(url, body)
        if method == self.HTTPMethod.PUT:
            return self._put_request(url, body)
        if get_file:
            return self._get_file_request(url)
        return self._get_request(url)

    def _get_request(self, url):
        headers = self._create_default_headers()
        return requests.get(url, headers=headers, proxies=self.proxy)

    def _get_file_request(self, url):
        headers = self._create_default_headers()
        return requests.get(url, headers=headers, proxies=self.proxy, stream=True)

    def _post_request(self, url, body):
        headers = self._create_default_headers()
        if body:
            data = self.serialize_request(body)
        return requests.post(url, headers=headers, data=data, proxies=self.proxy)

    def _put_request(self, url, body):
        headers = self._create_default_headers()
        if body:
            data = self.serialize_request(body)
        return requests.put(url, headers=headers, data=data, proxies=self.proxy)

    def _post_file_request(self, url, file_path):
        headers = self._create_default_headers()
        del headers['Content-Type']
        if file_path:
            size = os.path.getsize(file_path)
            if size > self.MAX_FILE_SIZE_IN_BYTES:
                raise Exception("File size should not exceed {} MB".format(self.MAX_FILE_SIZE_IN_BYTES / 1024 / 1024))
            files = {'file': open(file_path, 'rb')}
        return requests.post(url, headers=headers, files=files, proxies=self.proxy)

    def _create_default_headers(self):
        headers = {
            'User-Agent': '{}'.format(self._user_agent),
            'Authorization': 'Bearer {}'.format(self.access_token),
            'Content-Type': 'application/json'
        }
        return headers

    def _get_response(self, response, get_file, request):
        if isinstance(request, req.FormRegisterRequest) and getattr(request, 'format', 'json') == "csv":
            res = resp.FormRegisterResponse()
            res.csv = response.text
            return res
        if get_file:
            return response
        return response.json()

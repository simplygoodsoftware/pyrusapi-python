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
import requests
from .models import responses as resp, requests as req

class PyrusAPI(object):

    class HTTPMethod(Enum):
        GET = "GET"
        POST = "POST"

    _host = 'api.pyrus.com'
    _base_path = '/v4'
    access_token = None
    _protocol = 'https'
    _api_name = 'Pyrus'
    format = 'json'
    _user_agent = 'Pyrus API python client v 1.0.0'
    proxy = None

    def __init__(self, login=None, security_key=None, access_token=None, proxy=None):
        self.security_key = security_key
        self.access_token = access_token
        self.login = login
        if proxy:
            self.proxy = {'http': proxy}

    def auth(self, login=None, security_key=None):
        if login:
            self.login = login
        if security_key:
            self.security_key = security_key
        response = self._auth()
        return resp.AuthResponse(**response)

    def get_forms(self):
        url = self._create_url('/forms')
        response = self._perform_get_request(url)
        return resp.FormsResponse(**response)

    def get_registry(self, form_id, form_register_request=None):
        url = self._create_url(f'/forms/{form_id}/register')
        if form_register_request:
            if not isinstance(form_register_request, req.FormRegisterRequest):
                raise TypeError('form_register_request must be an instance '
                                'of models.requests.FormRegisterRequest')
            response = self._perform_post_request(url, form_register_request)
        else:
            response = self._perform_get_request(url)

        return resp.FormRegisterResponse(**response)

    def get_contacts(self):
        url = self._create_url('/contacts')
        response = self._perform_get_request(url)
        return resp.ContactsResponse(**response)

    def get_catalog(self, catalog_id):
        try:
            int(catalog_id)
        except ValueError:
            raise Exception("catalog_id should be valid int")

        url = self._create_url(f'/catalogs/{catalog_id}')
        response = self._perform_get_request(url)
        return resp.CatalogResponse(**response)

    def get_form(self, form_id):
        try:
            int(form_id)
        except ValueError:
            raise Exception("form_id should be valid int")

        url = self._create_url(f'/forms/{form_id}')
        response = self._perform_get_request(url)
        return resp.FormResponse(**response)

    def get_task(self, task_id):
        try:
            int(task_id)
        except ValueError:
            raise Exception("task_id should be valid int")

        url = self._create_url(f'/tasks/{task_id}')
        response = self._perform_get_request(url)
        return resp.TaskResponse(**response)

    def comment_task(self, task_id, task_comment_request):
        try:
            int(task_id)
        except ValueError:
            raise Exception("task_id should be valid int")
        url = self._create_url(f'/tasks/{task_id}/comments')
        if not isinstance(task_comment_request, req.TaskCommentRequest):
            raise TypeError('form_register_request must be an instance '
                            'of models.requests.TaskCommentRequest')
        response = self._perform_post_request(url, task_comment_request)
        return resp.TaskResponse(**response)

    def create_task(self, create_task_request):
        url = self._create_url('/tasks')
        if not isinstance(create_task_request, req.CreateTaskRequest):
            raise TypeError('create_task_request must be an instance '
                            'of models.requests.CreateTaskRequest')
        response = self._perform_post_request(url, create_task_request)
        return resp.TaskResponse(**response)

    def upload_file(self, file_path):
        url = self._create_url('/files/upload')
        response = self._perform_request_with_retry(url, self.HTTPMethod.POST, file_path=file_path)
        return resp.UploadResponse(**response)

    def _auth(self):
        url = self._create_url('/auth')
        headers = {
            'User-Agent': f'{self._user_agent}',
            'Content-Type': f'application/json'
        }
        params = {
            'login': self.login,
            'security_key': self.security_key
        }
        auth_response = requests.get(url, headers=headers, params=params)
        # pylint: disable=no-member
        if auth_response.status_code == requests.codes.ok:
            response = auth_response.json()
            self.access_token = response['access_token']
        else:
            response = auth_response.json()
            self.access_token = None

        return response

    def _create_url(self, url):
        return f"{self._protocol}://{self._host}{self._base_path}{url}"

    def _perform_get_request(self, url):
        return self._perform_request_with_retry(url, self.HTTPMethod.GET)

    def _perform_post_request(self, url, body=None):
        return self._perform_request_with_retry(url, self.HTTPMethod.POST, body)

    def _perform_request_with_retry(self, url, method, body=None, file_path=None):
        if not isinstance(method, self.HTTPMethod):
            raise TypeError('method must be an instanse of HTTPMethod Enum.')

        #try auth if no access token
        if not self.access_token:
            response = self._auth()
            if not self.access_token:
                return response

        #try to call api method
        response = self._perform_request(url, method, body, file_path)
        #if 401 try auth and call method again
        if response.status_code == 401:
            response = self._auth()
            #if failed return auth response
            if not self.access_token:
                return response

            response = self._perform_request(url, method, body, file_path)
        return response.json()

    def _perform_request(self, url, method, body, file_path):
        if method == self.HTTPMethod.POST:
            if file_path:
                response = self._post_file_request(url, file_path)
            else:
                response = self._post_request(url, body)
        else:
            response = self._get_request(url)
        return response

    def _get_request(self, url):
        headers = self._create_default_headers()
        return requests.get(url, headers=headers, proxies=self.proxy)

    def _post_request(self, url, body):
        headers = self._create_default_headers()
        if body:
            data = jsonpickle.dumps(body, unpicklable=False).encode('utf-8')
        return requests.post(url, headers=headers, data=data, proxies=self.proxy)

    def _post_file_request(self, url, file_path):
        headers = self._create_default_headers()
        del headers['Content-Type']
        if file_path:
            files = {'file': open(file_path, 'rb')}
        return requests.post(url, headers=headers, files=files, proxies=self.proxy)

    def _create_default_headers(self):
        headers = {
            'User-Agent': f'{self._user_agent}',
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        return headers

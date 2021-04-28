import json

from distutils.version import LooseVersion

try:
  from urllib.request import urlopen
  from urllib.parse import urlencode
  from urllib.error import HTTPError
except ImportError:
  from urllib import urlopen
  from urllib import urlencode
  from urllib2 import HTTPError


class Response(object):

  def __init__(self, data=None, message=None, error=False):
    self.data    = data
    self.error   = error
    self.success = not bool(error)
    self.message = self._parse_message(message)

  def _parse_message(self, message):
    if isinstance(message, str):
      message = message.split(']')[-1]
      message = message.lstrip('<').rstrip('>').strip()
      message = '%s%s' % (message[0].upper(), message[1:])
    elif isinstance(message, dict):
      message = message.get('message', 'internal server error')

    return message


class Request(object):

  def __init__(self, host, port=None, scheme='http', api_version=None):
    self.base = self._geturl_base(scheme, host, str(port))
    self.api_version = api_version

  def get(self, req_url, **params):
    apiurl = self._geturl(req_url, **params)
    return self._request(apiurl)

  def _geturl(self, path, **params):
    params = self._append_api_version(params)
    params = dict(map(self._parse_param, params.items()))
    params = urlencode(params)
    apiurl = str(path).replace(self.base, '').strip('/')

    return '{0}/{1}?{2}'.format(self.base, apiurl, params)

  def _request(self, req_url):
    try:
      response = self._parse_json(urlopen(req_url).read())
    except (IOError, HTTPError) as error:
      response = { 'result': None, 'error': str(error) }

    return self._generate_response(response)

  def _generate_response(self, output):
    result = output.get('result') or output.get('response')
    error  = output.get('error')

    return Response(data=result, error=bool(error), message=error)

  def _geturl_base(self, scheme, host, port):
    if scheme and not host.startswith(scheme):
      host = '{0}://{1}'.format(scheme, host)

    if port and not host.endswith(port):
      host = '{0}:{1}'.format(host, port)

    return host

  def _append_api_version(self, params):
    if self.api_version and not 'api_version' in params:
      params['api_version'] = self.api_version

    return params

  def _get_response_key(self, response, key):
    if response.success:
      return response.data.get(key)

  def _parse_json(self, string):
    try:
      return json.loads(string)
    except (IOError, ValueError):
      return {}

  def _parse_param(self, param):
    key, value = param

    if isinstance(value, bool):
      value = int(value)

    return (key, value)


class Server(Request):

  def __init__(self, host, port=6878, scheme='http', api_token=None, api_version=None):
    Request.__init__(self, host, port, scheme, api_version)

    self.api_token = api_token

  def getservice(self, **params):
    return self.get('webui/api/service', format='json', **params)

  def getversion(self):
    return self.getservice(method='get_version')

  def getserver(self, **params):
    return self.get('server/api', **params)

  def gettoken(self):
    return self.getserver(method='get_api_access_token')

  def getsearch(self, **params):
    return self.getserver(method='search', token=self.token, **params)

  def getstream(self, **params):
    is_hls = params.pop('hls', False)
    apiurl = 'manifest.m3u8' if is_hls else 'getstream'

    if self.version and LooseVersion(self.version) < LooseVersion('3.1.29'):
      params['sid'] = params.pop('pid')

    return self.get('ace/{0}'.format(apiurl), format='json', **params)

  def getbroadcast(self, manifest_url):
    return self.get('hls/manifest.m3u8', format='json', manifest_url=manifest_url)

  @property
  def version(self):
    response = self.getversion()
    return self._get_response_key(response, 'version')

  @property
  def available(self):
    return bool(self.version)

  @property
  def token(self):
    if not self.api_token:
      response = self.gettoken()
      self.api_token = self._get_response_key(response, 'token')

    return self.api_token

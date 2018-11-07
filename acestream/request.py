from urllib import request
from urllib.parse import urlencode
from urllib.error import URLError

from acestream.utils import parse_json


class Response(object):

  def __init__(self, data=None, error=False, message=None):
    self.data    = data
    self.error   = error
    self.success = not error
    self.message = message


class Request(object):

  def __init__(self, schema='http', host='127.0.0.1', port=6878):
    self.base    = self._getapi_base(schema, host, port)
    self.version = self._getapi_version()
    self.token   = self._getapi_token()

  def get(self, url, **params):
    apiurl = self._geturl(url, **params)
    return self._request(apiurl)

  def getservice(self, **params):
    return self.get('webui/api/service', format='json', **params)

  def getversion(self):
    return self.getservice(method='get_version')

  def getapi(self, **params):
    return self.get('server/api', **params)

  def gettoken(self):
    return self.getapi(method='get_api_access_token')

  def getstream(self, **params):
    return self.get('ace/getstream', format='json', **params)

  def _geturl(self, path, **params):
    params = urlencode(params)
    apiurl = str(path).replace('%s/' % self.base, '')

    return '{0}/{1}?{2}'.format(self.base, apiurl, params)

  def _request(self, url):
    try:
      response = request.urlopen(url).read()
      return self._generate_response(response)
    except (ConnectionRefusedError, URLError):
      return Response(error='noconnect', message='engine unavailable')

  def _generate_response(self, output):
    output = parse_json(output)
    error  = output.get('error', 'content unavailable')
    result = output.get('result') or output.get('response')

    if result:
      return Response(data=result)
    else:
      return Response(message=error, error='unavailable')

  def _getapi_base(self, schema, host, port):
    return '{0}://{1}:{2}'.format(schema, host, port)

  def _getapi_version(self):
    response = self.getversion()

    if response.success:
      return response.data.get('version')

  def _getapi_token(self):
    response = self.gettoken()

    if response.success:
      return response.data.get('token')

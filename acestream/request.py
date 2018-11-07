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
    self.base = '{0}://{1}:{2}'.format(schema, host, port)

  def get(self, url, **params):
    apiurl = self._geturl(url, **params)
    return self._request(apiurl)

  def getservice(self, **params):
    return self.get('webui/api/service', **params, format='json')

  def getversion(self):
    return self.getservice(method='get_version')

  def getstream(self, **params):
    return self.get('ace/getstream', **params, format='json')

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

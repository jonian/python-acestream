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
    getkey = params.pop('success_key', 'response')
    apiurl = self._geturl(url, **params)

    return self._request(apiurl, getkey)

  def getservice(self, **params):
    apiurl = 'webui/api/service'
    return self.get(apiurl, **params, format='json', success_key='result')

  def getversion(self):
    return self.getservice(method='get_version')

  def getstream(self, **params):
    return self.get('ace/getstream', **params, format='json')

  def _geturl(self, path, **params):
    params = urlencode(params)
    apiurl = str(path).replace('%s/' % self.base, '')

    return '{0}/{1}?{2}'.format(self.base, apiurl, params)

  def _request(self, url, success_key):
    try:
      response = request.urlopen(url).read()
      return self._generate_response(response, success_key)
    except (ConnectionRefusedError, URLError):
      return Response(error='noconnect', message='engine unavailable')

  def _generate_response(self, output, success_key):
    output   = parse_json(output)
    error    = output.get('error', 'content unavailable')
    response = output.get(success_key, False)

    if response:
      return Response(data=response)
    else:
      return Response(error='unavailable', message=error)

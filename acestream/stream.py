from acestream.object import Extendable
from acestream.object import Observable

from acestream.utils import is_acestream
from acestream.utils import sha1_hexdigest


class Stream(Extendable, Observable):

  is_http             = False
  is_stream           = False
  is_live             = False
  playback_session_id = None
  command_url         = None
  playback_url        = None
  stat_url            = None
  error               = None
  error_message       = None

  def __init__(self, api_request, stream_url):
    self.api = api_request
    self.url = stream_url

    self._parse_stream_params()

  @property

  def params(self):
    if self.is_stream:
      return { 'sid': self.sid, 'id': self.id }

    if self.is_http:
      return { 'sid': self.sid, 'url': self.url }

  def start(self):
    response = self.api.getstream(**self.params)
    self._set_response_to_values(response)

    return response.success

  def stop(self):
    response = self.api.get(self.command_url, method='stop')
    return response == 'ok'

  def _set_response_to_values(self, response):
    if response.success:
      self._set_attrs_to_values(response.data)
    else:
      self._set_error_to_values(response)

  def _set_error_to_values(self, data):
    self.error         = data.error
    self.error_message = data.message

  def _parse_stream_params(self):
    self.is_http   = self.url.startswith('http')
    self.is_stream = is_acestream(self.url)

    if self.is_stream and not self.url.startswith('acestream'):
      self.url = 'acestream://{0}'.format(self.url)

    if self.is_stream:
      self.id  = self.url.split('://')[-1]
      self.sid = sha1_hexdigest(self.id)

    if self.is_http:
      self.sid = sha1_hexdigest(self.url)

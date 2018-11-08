from acestream.object import Extendable
from acestream.object import Observable

from acestream.utils import sha1_hexdigest


class Stream(Extendable, Observable):

  is_live             = None
  playback_session_id = None
  command_url         = None
  playback_url        = None
  stat_url            = None
  error               = None
  error_message       = None

  def __init__(self, request, id=None, url=None, infohash=None):
    self.api = request

    self._check_required_args(id=id, url=url, infohash=infohash)
    self._parse_stream_params(id=id, url=url, infohash=infohash)

  def start(self):
    response = self.api.getstream(sid=self.sid, **self.params)
    self._set_response_to_values(response)

    return response.success

  def stop(self):
    response = self.api.get(self.command_url, method='stop')
    return response.data == 'ok'

  @property

  def params(self):
    params = { 'id': self.id, 'url': self.url, 'infohash': self.infohash }
    params = dict(filter(lambda item: item[1] is not None, params.items()))

    return params

  def _set_response_to_values(self, response):
    if response.success:
      self._set_attrs_to_values(response.data)
    else:
      self._set_error_to_values(response)

  def _set_error_to_values(self, data):
    self.error         = data.error
    self.error_message = data.message

  def _check_required_args(self, **kwargs):
    values = list(filter(None, kwargs.values()))
    params = "'id' or 'url' or 'infohash'"

    if not any(values):
      banner = '__init__() missing 1 required positional argument'
      raise TypeError('{0}: {1}'.format(banner, params))

    if len(values) > 1:
      banner = '__init__() too many positional arguments, provide only one of'
      raise TypeError('{0}: {1}'.format(banner, params))

  def _parse_stream_params(self, **kwargs):
    self.sid = sha1_hexdigest(kwargs)
    self._set_attrs_to_values(kwargs)

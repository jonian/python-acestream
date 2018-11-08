from acestream.object import Extendable
from acestream.stream import Stream


class ChannelResult(Extendable):

  total = 0
  name  = None
  icon  = None
  epg   = None
  items = None

  def __init__(self, request, data):
    self._generate_items(request, data.pop('items'))
    self._set_attrs_to_values(data)
    self._parse_attributes()

  def _generate_items(self, request, results):
    self.items = [StreamResult(request, i) for i in results]

  def _parse_attributes(self):
    self.name  = self.name.strip()
    self.total = len(self.items)


class StreamResult(Extendable):

  infohash                = None
  name                    = None
  channel_id              = None
  bitrate                 = None
  categories              = None
  availability_updated_at = None
  availability            = None
  status                  = None
  in_playlist             = None
  stream                  = None

  def __init__(self, request, data):
    self._generate_stream(request, data.get('infohash'))
    self._set_attrs_to_values(data)
    self._parse_attributes()

  def _generate_stream(self, request, infohash):
    self.stream = Stream(request, infohash=infohash)

  def _parse_attributes(self):
    self.name = self.name.strip()


class Search(Extendable):

  total   = 0
  time    = 0
  results = None

  def __init__(self, request):
    self.api = request

  def query(self, **params):
    channels = params.get('group_by_channels')
    response = self.api.getsearch(**params)

    if response.success:
      results = response.data.pop('results')
      self._generate_results(channels, results)
      self._set_attrs_to_values(response.data)

  def _generate_results(self, channels, results):
    if channels:
      self.results = [ChannelResult(self.api, i) for i in results]
    else:
      self.results = [StreamResult(self.api, i) for i in results]

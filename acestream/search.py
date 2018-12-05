import math

from acestream.object import Extendable
from acestream.stream import Stream


class ChannelResult(Extendable):

  def __init__(self, server, data):
    Extendable.__init__(self)

    self.total = 0
    self.name  = None
    self.icon  = None
    self.epg   = None
    self.items = None

    self._generate_items(server, data.pop('items'))
    self._set_attrs_to_values(data)
    self._parse_attributes()

  def _generate_items(self, server, results):
    self.items = [StreamResult(server, i) for i in results]

  def _parse_attributes(self):
    self.name  = self.name.strip()
    self.total = len(self.items)


class StreamResult(Extendable):

  def __init__(self, server, data):
    Extendable.__init__(self)

    self.infohash                = None
    self.name                    = None
    self.channel_id              = None
    self.bitrate                 = None
    self.categories              = None
    self.availability_updated_at = None
    self.availability            = None
    self.status                  = None
    self.in_playlist             = None
    self.stream                  = None

    self._generate_stream(server, data.get('infohash'))
    self._set_attrs_to_values(data)
    self._parse_attributes()

  def _generate_stream(self, server, infohash):
    self.stream = Stream(server, infohash=infohash)

  def _parse_attributes(self):
    self.name = self.name.strip()


class Search(Extendable):

  def __init__(self, server, **params):
    Extendable.__init__(self)

    self.total_pages = 0
    self.total       = 0
    self.time        = 0
    self.results     = None
    self.server      = server
    self.params      = params
    self.page        = int(params.pop('page', 1))
    self.page_size   = int(params.pop('page_size', 10))
    self.groups      = bool(params.pop('group_by_channels', False))

  def get(self, page=1):
    self.page = page
    response  = self.server.getsearch(**self.query_params)

    if response.success:
      results = response.data.pop('results')
      self._generate_results(results)

      self._set_attrs_to_values(response.data)
      self.total_pages = math.ceil(self.total / self.page_size)

  @property
  def query_params(self):
    params = self.params

    params['page']              = self.page
    params['page_size']         = self.page_size
    params['group_by_channels'] = self.groups

    return params

  def _generate_results(self, results):
    if self.groups:
      self.results = [ChannelResult(self.server, i) for i in results]
    else:
      self.results = [StreamResult(self.server, i) for i in results]

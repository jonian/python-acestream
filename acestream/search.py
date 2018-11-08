import math

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

  params      = None
  groups      = False
  page        = 1
  page_size   = 10
  total_pages = 0
  total       = 0
  time        = 0
  results     = None

  def __init__(self, request, **params):
    self.api       = request
    self.params    = params
    self.page      = int(params.pop('page', 1))
    self.page_size = int(params.pop('page_size', 10))
    self.groups    = bool(params.pop('group_by_channels', False))

  def get(self, page=1):
    self.page = page
    response  = self.api.getsearch(**self.query_params)

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
      self.results = [ChannelResult(self.api, i) for i in results]
    else:
      self.results = [StreamResult(self.api, i) for i in results]

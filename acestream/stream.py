import time
import hashlib

from threading import Thread
from acestream.object import Extendable
from acestream.object import Observable


class Stats(Extendable, Observable):

  def __init__(self, server):
    Extendable.__init__(self)
    Observable.__init__(self)

    self.stat_url       = None
    self.status         = None
    self.peers          = 0
    self.speed_down     = 0
    self.speed_up       = 0
    self.downloaded     = 0
    self.uploaded       = 0
    self.progress       = 0
    self.total_progress = 0
    self.server         = server

  def watch(self, stat_url):
    self.stat_url = stat_url
    poller_thread = Thread(target=self._poll_stats)

    poller_thread.setDaemon(True)
    poller_thread.start()

  def stop(self):
    self.stat_url = None

  def update(self):
    response = self.server.get(self.stat_url)
    self._set_response_to_values(response)

  def _set_response_to_values(self, response):
    if response.success:
      self._set_attrs_to_values(response.data)
      self.emit('updated')

  def _poll_stats(self):
    while self.stat_url:
      time.sleep(1)
      self.update()


class Stream(Extendable, Observable):

  def __init__(self, server, id=None, url=None, infohash=None):
    Extendable.__init__(self)
    Observable.__init__(self)

    self.status              = None
    self.is_live             = None
    self.playback_session_id = None
    self.command_url         = None
    self.playback_url        = None
    self.stat_url            = None
    self.server              = server
    self.stats               = Stats(server)

    self._check_required_args(id=id, url=url, infohash=infohash)
    self._parse_stream_params(id=id, url=url, infohash=infohash)

  def start(self):
    response = self.server.getstream(sid=self.sid, **self.params)

    if response.success:
      self._set_attrs_to_values(response.data)
      self._start_watchers()

      self.emit('started')
    else:
      self.emit('error', response.message)

  def stop(self):
    response = self.server.get(self.command_url, method='stop')

    if response.success:
      self._stop_watchers()
      self.emit('stopped')
    else:
      self.emit('error', response.message)

  @property
  def params(self):
    params = { 'id': self.id, 'url': self.url, 'infohash': self.infohash }
    params = dict(filter(lambda item: item[1] is not None, params.items()))

    return params

  def _start_watchers(self):
    if self.stat_url:
      self.stats.watch(self.stat_url)
      self.stats.connect('updated', self._on_stats_update)

  def _stop_watchers(self):
    self.stats.stop()

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
    sid_args = list(filter(None, kwargs.values()))
    self.sid = hashlib.sha1(sid_args[0].encode('utf-8')).hexdigest()

    self._set_attrs_to_values(kwargs)

  def _on_stats_update(self):
    prev_status = self.status
    self.status = self.stats.status

    self.emit('stats::updated')

    if prev_status != self.status:
      self.emit('status::changed')

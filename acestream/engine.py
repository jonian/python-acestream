import os
import signal
import threading
import subprocess

from acestream.object import Extendable
from acestream.object import Observable


class Engine(Extendable, Observable):

  bin     = None
  options = None
  process = None

  def __init__(self, request, bin, **options):
    self.api     = request
    self.bin     = bin
    self.options = options

  def start(self, **kwargs):
    if not self.running:
      thread = threading.Thread(target=self._start_proccess, args=[kwargs])
      thread.start()

  def stop(self):
    if self.process:
      os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
      self.process = None

  @property

  def running(self):
    return bool(self.process or self.api.version)

  @property

  def process_args(self):
    options = list(map(self._parse_option, self.options.items()))
    return [*self.bin.split(' '), *options]

  def _start_proccess(self, kwargs):
    kwargs['preexec_fn'] = os.setsid

    try:
      self.process = subprocess.Popen(self.process_args, **kwargs)
    except OSError:
      self.process = None

  def _parse_option(self, option):
    key, val = option
    argument = '--{0}'.format(key.replace('_', '-'))

    if not isinstance(val, bool):
      argument = '{0} {1}'.format(argument, val)

    return argument

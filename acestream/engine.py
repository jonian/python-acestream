import os
import signal
import subprocess

from threading import Thread
from acestream.object import Observable


class Engine(Observable):

  def __init__(self, bin, **options):
    Observable.__init__(self)

    self.process = None
    self.bin     = bin
    self.options = options

  def start(self, daemon=True, **kwargs):
    if not self.running:
      thread = Thread(target=self._start_process, kwargs=kwargs)
      thread.setDaemon(daemon)
      thread.start()

  def stop(self):
    if self.process:
      os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)

      self.process = None
      self.emit('terminated')

  @property
  def running(self):
    return bool(self.process)

  @property
  def process_args(self):
    options = self.bin.split()

    for (key, value) in self.options.items():
      options.append('--{0}'.format(key.replace('_', '-')))

      if not isinstance(value, bool):
        options.append(str(value))

    return options

  def _start_process(self, **kwargs):
    kwargs['preexec_fn'] = os.setsid

    try:
      self.process = subprocess.Popen(self.process_args, **kwargs)
      self.emit('started')
      self.process.communicate()

      self.process = None
      self.emit('terminated')
    except OSError as error:
      self.process = None
      self.emit('error', str(error))

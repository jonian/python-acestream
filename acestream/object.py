class Extendable(object):

  def _set_attrs_to_values(self, data={}):
    if isinstance(data, dict):
      for key in data.keys():
        if not hasattr(self, key) or not callable(getattr(self, key)):
          setattr(self, key, data[key])


class Observable(object):

  def __init__(self):
    self._events = []

  def connect(self, event_name, callback_fn):
    self._events.append({ 'event_name': event_name, 'callback_fn': callback_fn })

  def emit(self, event_name, *callback_args):
    for event in self._events:
      if event['event_name'] == event_name:
        event['callback_fn'](*callback_args)

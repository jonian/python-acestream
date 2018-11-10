#!/usr/bin/env python

import os
import time
import subprocess

from acestream.server import Server
from acestream.engine import Engine
from acestream.stream import Stream

try:
  # Create an engine instance
  engine = Engine('acestreamengine', client_console=True)

  # Connect to a remote server
  server = Server(host='streams.com', port=6880)

  # If the remote server is not available, connect to a local server
  if not server.available:
    server = Server(host='127.0.0.1', port=6878)

    # Start engine if the local server is not available
    if not server.available:
      engine.start()

      # Wait for engine to start
      while not engine.running:
        time.sleep(1)

  # Start a stream using an acestream channel ID
  stream = Stream(server, id='ff36fce40a7d2042e327eaf9f215a1e9cb622b56')
  stream.start()

  # Open a media player to play the stream
  player = subprocess.Popen(['mpv', stream.playback_url], preexec_fn=os.setsid)

  # Wait for player to close and stop the stream
  player.communicate()
  stream.stop()

  # Stop acestream engine
  engine.stop()
except KeyboardInterrupt:
  engine.stop()
  print('\n\nExiting...')

#!/usr/bin/env python

import time
import subprocess

from acestream.server import Server
from acestream.engine import Engine
from acestream.stream import Stream

player = None
stream = None
engine = None

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
  stream = Stream(server, id='dce1975f071782d269563c2f83d813c38b5f5205')
  stream.start()

  # Open a media player to play the stream
  player = subprocess.Popen(['mpv', stream.playback_url])

  # Wait for player to close and stop the stream
  player.communicate()
  stream.stop()

  # Stop acestream engine
  engine.stop()
except KeyboardInterrupt:
  if player: player.kill()
  if stream: stream.stop()
  if engine: engine.stop()

  print('\n\nExiting...')

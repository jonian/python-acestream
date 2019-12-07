#!/usr/bin/env python

import time
import random
import subprocess

from acestream.server import Server
from acestream.engine import Engine
from acestream.search import Search

try:
  # Create an engine instance
  engine = Engine('acestreamengine', client_console=True)

  # Connect to a local server
  server = Server(host='127.0.0.1', port=6878)

  # Start engine if the local server is not available
  if not server.available:
    engine.start(stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for engine to start
    while not engine.running:
      time.sleep(1)

  # Start a search for the sport category
  search = Search(server, category='sport')
  search.get(page=1)

  # Iterate and print search results
  for result in search.results:
    print("%40s %10s %40s" % (result.name, result.bitrate, result.infohash))

  # Start a random stream from the search results
  stream = random.choice(search.results).stream
  stream.start(hls=True, transcode_audio=True)

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

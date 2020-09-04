# Python AceStream
Python interface to interact with the AceStream [Engine](https://wiki.acestream.media/Streaming), [HTTP API](https://wiki.acestream.media/Engine_HTTP_API) and [Search API](https://wiki.acestream.media/Search_API).

## Installation
```
pip install acestream
```

## Usage
```python
import time
import subprocess

from acestream.server import Server
from acestream.engine import Engine
from acestream.stream import Stream

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
player = subprocess.Popen(['mpv', stream.playback_url])

# Wait for player to close and stop the stream
player.communicate()
stream.stop()

# Stop acestream engine
engine.stop()
```

## Search
```python
import time
import random
import subprocess

from acestream.server import Server
from acestream.engine import Engine
from acestream.search import Search

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
```

## Contributing
Bug reports and pull requests are welcome on GitHub at https://github.com/jonian/python-acestream.

## License
Python AceStream is available as open source under the terms of the [GPLv3](http://www.gnu.org/licenses/gpl-3.0.en.html)

# Python AceStream
Python interface to interact with the AceStream Engine and the HTTP API.

## Installation
```
pip install python-mpv
```

## Usage
```python
import subprocess

from acestream.server import Server
from acestream.engine import Engine

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

# Start a stream with a acestream channel ID
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

## Contributing
Bug reports and pull requests are welcome on GitHub at https://github.com/jonian/python-acestream.

## License
Python AceStream is available as open source under the terms of the [GPLv3](http://www.gnu.org/licenses/gpl-3.0.en.html)

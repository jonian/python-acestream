import re
import json
import hashlib


def parse_json(string):
  try:
    return json.loads(string)
  except (IOError, ValueError):
    return {}


def sha1_hexdigest(string):
  return hashlib.sha1(string.encode('utf-8')).hexdigest()


def is_acestream(string):
  pattern = re.compile("(acestream\:\/\/)?[\w\d]{40}")
  return bool(pattern.match(string))

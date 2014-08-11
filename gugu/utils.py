import re

def clean_newlines(text):
  return re.sub(r' *\r?\n *', '\n', text.strip())

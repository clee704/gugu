import re

GUGU_PATTERN = r'\b\w{2}\s+\w{3}\s+\w{3}\s+\w{6}\s+\w{4}\s+\w{4}\s+\w{3}\s+\w{3}\b'

class GuguPipeline(object):
  def process_item(self, item, spider):
    if re.search(GUGU_PATTERN, item['lyrics']):
      item['match'] = 'true'
    else:
      item['match'] = 'false'
    return item

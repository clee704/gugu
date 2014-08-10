import re

GUGU_PATTERN = r'\b..\s+...\s+...\s+......\s+....\s+....\s+...\s+...\b'

class GuguPipeline(object):
  def process_item(self, item, spider):
    if re.search(GUGU_PATTERN, item['lyrics']):
      item['match'] = 'true'
    else:
      item['match'] = 'false'
    return item

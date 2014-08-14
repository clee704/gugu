import logging
import re
from scrapy import log
from scrapy.mail import MailSender

GUGU_PATTERN = r'\b\w{2}\s+\w{3}\s+\w{3}\s+\w{6}\s+\w{4}\s+\w{4}\s+\w{3}\s+\w{3}\b'

class GuguPipeline(object):

  def __init__(self, mail_to):
    self.mailer = MailSender()
    self.mail_to = mail_to
    if mail_to:
      log.msg('Emails will be sent to %s' % mail_to, level=logging.INFO)

  @classmethod
  def from_settings(cls, settings):
    mail_to = settings['GUGU_PIPELINE_MAIL_TO']
    return cls(mail_to)

  def process_item(self, item, spider):
    if re.search(GUGU_PATTERN, item['lyrics']):
      item['match'] = 'true'
      self.send_email(item)
    else:
      item['match'] = 'false'
    return item

  def send_email(self, item):
    if not self.mail_to:
      return
    subject = "Found a match: {artist} - {title}".format(**item)
    body = """URL: {url}

{lyrics}
""".format(**item)
    self.mailer.send(to=[self.mail_to], subject=subject, body=body)

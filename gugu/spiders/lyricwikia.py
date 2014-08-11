import logging
import re

import lxml.html
import scrapy
from html2text import html2text
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from ..items import Song
from ..utils import clean_newlines

def remove_garbage(value):
  return re.sub(r'&+', '&', re.sub(r'ns\d+=\d+', '', value))

class LyricwikiaSpider(CrawlSpider):
  name = 'lyricwikia'
  allowed_domains = ['lyrics.wikia.com']
  start_urls = [
    'http://lyrics.wikia.com/Special:Search?search=99&fulltext=Search',
    'http://lyrics.wikia.com/Special:Search?search=pigeon&fulltext=Search',
  ]
  rules = [
    Rule(LinkExtractor(allow=(r'/Special:Search',), process_value=remove_garbage)),
    Rule(LinkExtractor(allow=(r'/.*:.*',),
                       deny=(r'/(Special|User|Category|Gracenote|LyricWiki|Help|Talk|.*_talk|LyricFind):',)),
         callback='parse_song'),
  ]

  def parse_song(self, response):
    song = Song()
    song['url'] = response.url
    if not response.css('.categories a[title="Category:Song"]'):
      self.log('not a song: %s' % response.url)
      return
    gracenoteid = response.css('#gracenoteid')
    if not gracenoteid:
      self.log('no #gracenoteid: %s' % response.url, level=logging.WARN)
      return
    song['artist'], song['title'] = gracenoteid.xpath('text()').extract()[0].split(':', 1)
    lyricboxes = response.css('.lyricbox').extract()
    lyrics = []
    for b in lyricboxes:
      lyricbox = lxml.html.fromstring(b)
      for e in lyricbox.cssselect('.rtMatcher'):
        e.drop_tree()
      lyrics.append(clean_newlines(html2text(lxml.html.tostring(lyricbox))))
    song['lyrics'] = '\n\n\n'.join(lyrics)
    if re.search(r'^\n*$', song['lyrics']):
      self.log('no lyrics: %s' % response.url, level=logging.WARN)
    yield song

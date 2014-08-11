import re

import scrapy
from html2text import html2text
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from ..items import Song
from ..utils import clean_newlines

class SonglyricsSpider(CrawlSpider):
  name = 'songlyrics'
  allowed_domains = ['songlyrics.com']
  start_urls = ['http://www.songlyrics.com/']
  rules = [
    Rule(LinkExtractor(allow=('/[a-z0]/(\d+)?',))),
    Rule(LinkExtractor(allow=('/[a-z-]+/[a-z-]+-lyrics/',),
                       deny=('/news/',)), callback='parse_song'),
    Rule(LinkExtractor(allow=('/[a-z-]+-lyrics/',))),
  ]

  def parse_song(self, response):
    song = Song()
    song['url'] = response.url
    song['title'] = re.sub(r'(.*) Lyrics', r'\1', response.css('.current').xpath('text()').extract()[0])
    song['artist'] = response.css('.pagetitle').xpath('.//a/text()').extract()[0]
    song['lyrics'] = clean_newlines(html2text(response.css('#songLyricsDiv').extract()[0]))
    yield song

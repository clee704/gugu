import re

import scrapy
from html2text import html2text
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from ..items import Song

class AzlyricsSpider(CrawlSpider):
  name = 'azlyrics'
  allowed_domains = ['azlyrics.com']
  start_urls = ['http://www.azlyrics.com/']
  rules = [
    Rule(LinkExtractor(allow=('/([a-z]|19)\.html',))),
    Rule(LinkExtractor(allow=('/([a-z]|19)/[a-z0-9_-]+\.html'))),
    Rule(LinkExtractor(allow=('/lyrics/[a-z0-9_-]+/[a-z0-9_-]+\.html')),
         callback='parse_song')
  ]

  def parse_song(self, response):
    song = Song()
    song['url'] = response.url
    song['title'] = response.xpath('//script').re('SongName = "([^"]+)"')[0]
    song['artist'] = response.xpath('//script').re('ArtistName = "([^"]+)"')[0]
    song['lyrics'] = re.sub(r' *\n *', '\n',
      html2text(response.xpath('//div[@style="margin-left:10px;margin-right:10px;"]').extract()[0]).strip())
    yield song

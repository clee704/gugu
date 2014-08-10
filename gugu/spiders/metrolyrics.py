import re

import scrapy
from html2text import html2text
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from ..items import Song

class MetroSpider(CrawlSpider):
  name = 'metrolyrics'
  allowed_domains = ['metrolyrics.com']
  start_urls = ['http://www.metrolyrics.com/artists-1.html']
  rules = [
    Rule(LinkExtractor(allow=('/artists-[a-z1](-\d+)?\.html',))),
    Rule(LinkExtractor(allow=('/[a-z-]+-(lyrics|overview|alpage-\d+)\.html',))),
    Rule(LinkExtractor(allow=('/[a-z-]+-lyrics-[a-z-]+\.html',),
                       deny=('/news-story-',)), callback='parse_song'),
  ]

  def parse_song(self, response):
    song = Song()
    song['url'] = response.url
    song['title'] = re.sub(r'(.*) Lyrics', r'\1', response.xpath('//h1/text()').extract()[0].strip())
    song['artist'] = re.sub(r'(.*) Lyrics', r'\1', response.xpath('//h2/text()').extract()[0].strip())
    song['lyrics'] = re.sub(r' *\n *', '\n', html2text(response.css('#lyrics-body-text').extract()[0]).strip())
    yield song

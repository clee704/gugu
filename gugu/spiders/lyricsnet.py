import re

import scrapy
from html2text import html2text
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from ..items import Song
from ..utils import clean_newlines

class LyricsnetSpider(CrawlSpider):
  name = 'lyricsnet'
  allowed_domains = ['lyrics.net']
  start_urls = ['http://www.lyrics.net/']
  rules = [
    Rule(LinkExtractor(allow=('/artist/[^/]+(/\d+)?',))),
    Rule(LinkExtractor(allow=('/album/\d+',))),
    Rule(LinkExtractor(allow=('/lyric/\d+',)), callback='parse_song'),
  ]

  def parse_song(self, response):
    song = Song()
    song['url'] = response.url
    song['title'] = response.css('.lyric-title').xpath('text()').extract()[0]
    song['artist'] = response.css('.lyric-artist a').xpath('text()').extract()[0]
    song['lyrics'] = clean_newlines(html2text(response.css('.lyric-body').extract()[0]))
    yield song

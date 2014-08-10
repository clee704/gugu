import scrapy

class Song(scrapy.Item):
  url = scrapy.Field()
  title = scrapy.Field()
  artist = scrapy.Field()
  lyrics = scrapy.Field()
  match = scrapy.Field()

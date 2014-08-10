BOT_NAME = 'gugu'

SPIDER_MODULES = ['gugu.spiders']
NEWSPIDER_MODULE = 'gugu.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
COOKIES_ENABLED = False
DOWNLOAD_DELAY = 5

ITEM_PIPELINES = {
  'gugu.pipelines.GuguPipeline': 100,
}

FEED_URI = 'file:///Users/choongmin/Downloads/gugu/%(name)s-%(time)s.xml'
FEED_FORMAT = 'xml'

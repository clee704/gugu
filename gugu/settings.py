BOT_NAME = 'gugu'

SPIDER_MODULES = ['gugu.spiders']
NEWSPIDER_MODULE = 'gugu.spiders'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/7.0.5 Safari/537.77.4'
COOKIES_ENABLED = False
DOWNLOAD_DELAY = 5

ITEM_PIPELINES = {
  'gugu.pipelines.GuguPipeline': 100,
}

FEED_URI = 'file:///Users/choongmin/Downloads/gugu.xml'
FEED_FORMAT = 'xml'

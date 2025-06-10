BOT_NAME = "reverse-pdf-scraper"

SPIDER_MODULES = ["app.spiders"]
NEWSPIDER_MODULE = "app.spiders"

ADDONS = {}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "reverse-pdf-scraper/1.0 (+mailto:your@email.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Enable or disable spider middlewares
SPIDER_MIDDLEWARES = {"scrapy.spidermiddlewares.depth.DepthMiddleware": 543}
DEPTH_LIMIT = 1
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = "scrapy.squeues.PickleFifoDiskQueue"
SCHEDULER_MEMORY_QUEUE = "scrapy.squeues.FifoMemoryQueue"

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 2.5
DOWNLOAD_TIMEOUT = 300

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept-Language": "en",
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "app.pipelines.ProcessingPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"

# Logging settings
LOG_LEVEL = "DEBUG"
LOG_FILE = "scrapy.log"

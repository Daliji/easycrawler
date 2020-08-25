# --coding:utf-8--
# 爬虫的一些信息

from crawler.crawler.uestc_news.crawler import Crawler as C3

# 爬虫列表
_crawlers = [
    C3
]

# 爬虫示例列表
crawlers = [_() for _ in _crawlers]
for idx, c in enumerate(crawlers):
    c.id = idx + 1

# --coding:utf-8--
# 电子科大 新闻爬虫

from crawler.crawler.crawler_base import CrawlerBase
from crawler.crawler.crawler_info import CrawlerInfo
from crawler.crawler.uestc_news.uestcnews import UESTCCrawler
from crawler.settings import log
import time


class Crawler(CrawlerBase):
    def __init__(self):
        self.crawler = UESTCCrawler()
        self.status = 2  # 1=正在运行 2=已停止 3=正在停止
        self.data_count = 0

    def start(self, *args, **kwargs):
        if self.status != 2:
            log.error("爬虫未完全停止")
            return

        i = 0
        self.status = 1
        while (self.status == 1):
            page_index = i % 10 + 1
            i += 1
            log.info('now get page {} .'.format(page_index))
            contents = self.crawler.page_contents(page_index)
            need_sleep = False
            if contents is None:
                log.error("page {} error, now sleep!".format(page_index))
                need_sleep = True
            else:
                if len(contents) == 0: continue
                self.crawler.save_to_db(contents)
                self.data_count += len(contents)
            if i == 10:
                log.info('爬取完成，爬虫进入睡眠，时间十分钟')
                need_sleep = True
            if need_sleep: time.sleep(600)
        self.status = 2

    def stop(self, *args, **kwargs):
        self.status = 3

    def info(self):
        self._info = CrawlerInfo(name='电子科大新闻网站爬虫',
                                 logo='https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=2236633412,1037915644&fm=26&gp=0.jpg',
                                 desc='电子科大新闻网站爬虫，实时获取电子科大新闻数据，爬取网站为：https://news.uestc.edu.cn')
        return self._info

    def state(self):
        return self.status

    def get_data_count(self):
        return len(self.crawler.url_list)

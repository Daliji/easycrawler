# --coding:utf-8--
# 电子科大 新闻爬虫

from bs4 import BeautifulSoup
from crawler.db.DBUtil import DBUtil
import time
from crawler.settings import log
import requests


class UESTCCrawler:
    def __init__(self):
        self.db = DBUtil()
        self.url_list = []  # 用于次爬取判重
        self.init_news_address()

    def _get_news_page_url(self, page_index):
        '''
        下一页新闻
        :return:
        '''
        url_head = 'https://news.uestc.edu.cn/'
        return url_head

    def page_contents(self, page_index):
        '''
        取得每一页的URL等信息
        :return:
        '''
        url_head = self._get_news_page_url(page_index)
        try:
            contents = []
            url_response = requests.get(url_head)
            url_soup = BeautifulSoup(url_response.text, "html.parser")
            news_menus = url_soup.find_all('a', class_="cell")
            for news_menu in news_menus:
                news_type = news_menu.get_text().replace('\n', '').strip()
                url_tail = news_menu.attrs['href']
                page_url = 'https://news.uestc.edu.cn' + str(url_tail) + '&page=' + str(page_index)
                response = requests.get(page_url)
                soup = BeautifulSoup(response.text, "html.parser")
                news = soup.select(' div[id="Degas_news_list"] > ul > li ')
                for list in news:
                    title = list.select(' h3 > a')[0].get_text().replace('\n', '').replace("'", r"\'").strip()
                    brief = list.find_all('p', class_="desc")[0].get_text().replace('\n', '').replace("'", r"\'").strip()
                    page_address = list.select(' h3 > a')[0]
                    address_a = page_address.attrs['href']
                    url = 'https://news.uestc.edu.cn' + str(address_a)
                    if url in self.url_list: continue
                    log.info('正在爬取：' + url)
                    page = requests.get(url)
                    contents_a = BeautifulSoup(page.text, "html.parser").find_all('div', class_="Degas_news_content")[0].contents[1]
                    content = str(contents_a).replace("'", r"\'")
                    create_time = list.find_all('span', class_="time")[0].get_text().replace('\n', '').strip()
                    item = {
                        'title': title,
                        'brief': brief,
                        'url': url,
                        'content': content,
                        'news_type': news_type,
                        'create_time': create_time
                    }
                    contents.append(
                        {'url': item['url'], 'title': item['title'], 'brief': item['brief'], 'content': item['content'],
                         'news_type': item['news_type'], 'create_time': item['create_time']})
                    self.url_list.append(item['url'])
            return contents
        except:
            return None

    def init_news_address(self):
        '''
        去除数据库中已有的url
        :return:
        '''
        address = self.db.query_db_as_list('select address from uestc_news')
        if address is None: return
        for ad in address:
            self.url_list.append(ad['address'])

    def save_to_db(self, data_list):
        log.info('insert into db ...')
        for d in data_list:
            try:
                sql = "insert into uestc_news(title,brief,address,content,create_time,corp_id,news_menu,index_name) values ('{}','{}','{}','{}','{}',{},'{}','{}')".format(
                    d['title'], d['brief'], d['url'], d['content'], d['create_time'] + " 00:00:00", 136,d['news_type'], 'uestc_news')
                self.db.update(sql)
            except:
                log.error('insert into db error: ' + d['url'])
                continue


def _run():
    c = UESTCCrawler()
    i = 0
    while (True):
        page_index = i % 10 + 1
        i += 1
        log.info('now get page {} .'.format(page_index))
        contents = c.page_contents(page_index)
        need_sleep = False
        if contents is None:
            log.error("page {} error, now sleep!".format(page_index))
            need_sleep = True
        else:
            c.save_to_db(contents)
        if i == 10:
            log.info('爬取完成，爬虫进入睡眠，时间十分钟')
            need_sleep = True
        if need_sleep: time.sleep(600)


if __name__ == '__main__':
    _run()

# --coding:utf-8--
# UESTS NEWS ES 操作

'''
数据存储于es不存储在内存，在数据量特别大，或者支持大量的Saas服务的时候可以用到。
es可以支持分布式、分片部署等，检索效率也较高
'''

from crawler.db.ESOperate import ES
from crawler.db.es_ops_base import EsBase
from bs4 import BeautifulSoup
from bs4 import Comment
import re
from crawler.db.DBUtil import DBUtil
from crawler.settings import log


class UESTCNEWS(EsBase):

    def __init__(self):
        self.es = ES(index_name=self.get_index_name(), delete_old_index=False)

    def query_data(self, sentence, topn=3):
        '''
        查询文档
        :param sentence:
        :param topn: 查询条数限制
        :return:
        '''

        query_map = {
            "query": {
                "match": {
                    "content": sentence
                }
            },
            "from": 0,
            "size": topn
        }
        res = self.es.freedom_search(query_map)
        res = res['hits']['hits']
        result = []
        for r in res:
            result.append(r['_source'])
        return result

    def load_data(self, *args, **kwargs):
        '''
        获取数据，这里是从数据库获取，要注意的是，需要将已有的数据与数据库的数据进行比较判重
        :param args:
        :param kwargs:
        :return:
        '''
        # 从数据库获取数据
        db = DBUtil()
        # TODO 需要根据ID或者address去重
        data = db.query_db_as_list(sql="select * from uestc_news")

        data_list = []
        for d in data:
            paragraphs = self.prepare_data(d['content']).split('\n')
            index = 0
            for p in paragraphs:
                if len(p.strip()) < 10: continue
                data_list.append({'doc_id': d['id'],
                                  "paragraph_index": index,
                                  'title': d['title'],
                                  'address': d['address'],
                                  "content": p.strip()})
                index += 1

        # 如果做了去重判断，则这里的 delete_old_index=False 即不删除旧数据
        self.es = ES(index_name=self.get_index_name(), delete_old_index=True)
        self.es.put_data(data_list)

    def get_index_name(self, *args, **kwargs):
        '''
        获取ES的index_name，注意不要与其他的ES index 重复
        :param args:
        :param kwargs:
        :return:
        '''
        return "uestc_news_es_content"

    def prepare_data(self, html_str):
        '''
        将html处理成段落的文本格式
        :param html_str:
        :return:
        '''
        soup = BeautifulSoup(html_str, features='lxml')
        # 过滤script
        for s in soup('script'): s.extract()
        # 过滤style
        for s in soup('style'): s.extract()
        # 过滤注释
        for ele in soup(text=lambda text: isinstance(text, Comment)): ele.extract()

        txt = soup.text
        txt = re.sub(r'\s\s+', '\n', txt)
        txt = '\n'.join([re.sub(r'\s+', ' ', s) for s in txt.split('\n')])
        return txt

    def get_mapping(self, *args, **kwargs):
        content_mapping = {
            "properties": {
                "doc_id": {  # 文档ID
                    "type": "long"
                },
                "paragraph_index": {  # 段落在文档中的序号
                    "type": "long"
                },
                "title": {  # 标题
                    "type": "text",
                    "analyzer": "ik_smart",
                    "search_analyzer": "ik_smart"
                },
                "content": {  # 内容
                    "type": "text",
                    "analyzer": "ik_smart",
                    "search_analyzer": "ik_smart",
                    "similarity": {
                        "my_custom_similarity": {
                            "type": "BM25",  # 使用BM25算法索引和查找
                            "k1": 2,
                            "b": 0.75
                        }
                    }
                },
                "address": {  # 文档地址
                    "type": "text",
                    "index": "false"
                }
            }
        }
        return content_mapping


# for test
if __name__ == '__main__':
    es = UESTCNEWS()
    es.load_data()
    log.info("############## search result ##################")
    log.info(es.query_data(sentence='习近平', topn=5))
    log.info("###############################################")

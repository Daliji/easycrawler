# coding:utf-8

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from crawler.settings import log, ES_URL


class ES:
    def __init__(self, index_name, delete_old_index=False):
        self.es = Elasticsearch(hosts=ES_URL, timeout=5000)
        self.index_name = index_name

        if delete_old_index:
            if self.es.indices.exists(index=index_name):
                self.es.indices.delete(index=index_name)

        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name)

        self.show_index_info()

    # 建议写入数据后刷新一次
    def flush(self):
        self.es.indices.flush(index=self.index_name)

    def show_index_info(self):
        '''
        取Mapping信息
        :return:
        '''
        _mapping = self.es.indices.get_mapping(index=self.index_name)
        log.info(_mapping)

    def put_mapping(self, mapping):
        self.es.indices.put_mapping(index=self.index_name, body=mapping)

    def put_data(self, data):
        actions = []

        for d in data:
            action = {
                "_index": self.index_name,
                "_source": d
            }
            if 'id' in d: action['_id'] = d['id']
            actions.append(action)

        success, _ = bulk(self.es, actions, index=self.index_name, raise_on_error=True)
        log.info('Performed %d actions' % success)

    def delete_data(self, query_map):
        '''
        根据query_map查询条件删除
        :param query_map:
        :return:
        '''
        if query_map is None:
            raise Exception("query map can not be None")
        res = self.es.delete_by_query(index=self.index_name, body=query_map)
        return res

    def delete_by_ids(self, ids):
        if ids is None or len(ids) == 0: return
        self.es.delete_by_query(index=self.index_name, body={
            "query": {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "default_field": "id",
                                "query": " OR ".join([str(_) for _ in ids])
                            }
                        }
                    ]
                }
            }
        })

    def search_from_id(self, id):
        res = self.es.get(index=self.index_name, id=id)
        return res

    def search_text(self, text):
        doc = {
            "query": {
                "query_string": {
                    "query": text
                }
            }
        }
        res = self.freedom_search(search_map=doc)
        return res

    def search_field(self, fields=None, pageIndex=1, pageSize=10, highlight=None):
        doc = {
            "query": {
                "match_all": {}
            }
        }

        if fields is not None:
            doc = {
                "query": {
                    "multi_match": fields
                }
            }

        if pageIndex is not None and pageSize is not None:
            doc['from'] = (pageIndex - 1) * pageSize
            doc['size'] = pageSize

        if highlight:
            doc['highlight'] = highlight

        res = self.freedom_search(search_map=doc)
        return res

    def get_all_content(self, pageIndex=1, pageSize=10):
        doc = {
            "query": {
                "match_all": {}
            }
        }
        if pageIndex is not None and pageSize is not None:
            doc['from'] = (pageIndex - 1) * pageSize
            doc['size'] = pageSize

        return self.freedom_search(search_map=doc)

    def freedom_search(self, search_map):
        result = self.es.search(index=self.index_name, body=search_map)
        return result

    def update_by_query(self, query_map):
        self.es.update_by_query(index=self.index_name, body=query_map)

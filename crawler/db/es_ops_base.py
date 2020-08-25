# --coding:utf-8--
# ES 数据操作基础类

import abc


class EsBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_mapping(self, *args, **kwargs):
        '''
        获取当前操作的es的mapping
        :return: dict map
        '''
        pass

    @abc.abstractmethod
    def get_index_name(self, *args, **kwargs):
        '''
        获取当前操作的 es index name
        :return: string
        '''
        pass

    @abc.abstractmethod
    def load_data(self, *args, **kwargs):
        '''
        获取数据
        :return: string
        '''
        pass

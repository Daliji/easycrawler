# --coding:utf-8--
# 爬虫基础类，所有爬虫都需要继承自此类

import abc


class CrawlerBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def start(self, *args, **kwargs):
        '''
        开始方法
        :return:
        '''
        pass

    @abc.abstractmethod
    def stop(self, *args, **kwargs):
        '''
        结束方法
        :return:
        '''
        pass

    @abc.abstractmethod
    def info(self):
        '''
        返回一个CrawlerInfo
        :return:
        '''
        pass

    @abc.abstractmethod
    def state(self):
        '''
        1=正在爬取;2=已停止
        :return:
        '''
        pass

    @abc.abstractmethod
    def get_data_count(self):
        '''
        获取爬取条数
        :return:
        '''
        pass

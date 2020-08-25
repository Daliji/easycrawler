# --coding:utf-8--
# 爬虫相关接口
from crawler.views.my_request import MyRequest
from crawler.crawler.settings import crawlers
import threading


def get_crawler_list(request):
    '''
    查询爬虫列表
    :param request:
    :return:
    '''
    request = MyRequest(request)
    assert request.error_code == 0
    data = []
    for c in crawlers:
        c_info = c.info()
        d = {
            'id': c.id,
            'name': c_info.name,
            'logo': c_info.logo,
            'desc': c_info.desc,
            'state': c.state(),
            'data_count': c.get_data_count()
        }
        data.append(d)
    return request.success_result(result=data)


def change_state(request):
    '''
    启动/停止 爬虫
    :param request:
    :return:
    '''
    request = MyRequest(request)
    assert request.error_code == 0
    id = int(request.get_param('id'))
    found = False
    for c in crawlers:
        if c.id == id:
            if c.state()==1:
                c.stop()
            else:
                threading.Thread(target=c.start, args=()).start()
            found = True
            break
    if found:
        return request.success_result()
    else:
        return request.get_result(code=1, msg='无此爬虫')

# --coding:utf-8--
# 检测服务器启动正常接口
from crawler.views.my_request import MyRequest

# 这个方法不要修改，用来测试是否启动成功的
def server_chk(request):
    request = MyRequest(request)
    assert request.error_code == 0
    return request.success_result()

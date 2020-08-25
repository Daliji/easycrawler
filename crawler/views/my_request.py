# --coding:utf-8--
from django.http import HttpResponse
import json


class MyRequest:
    '''
    error_code: 0=correct, 1=error
    '''

    def __init__(self, request):
        try:
            if request.method != 'POST':
                raise RuntimeError('request method error!')
            self.params = {}
            for p in request.POST: self.params[p] = request.POST[p]

            if request.content_type.lower().strip() == 'application/json':
                j_str = str(request.body, 'utf-8')
                j_dict = json.loads(j_str, encoding='utf-8')
                for jd in j_dict:
                    self.params[jd] = j_dict[jd]

            self.error_code = 0
        except:
            self.error_code = 1

    def get_param(self, key):
        if key not in self.params.keys():
            return None
        return self.params[key]

    def get_result(self, code, msg, result=None):
        '''
        封装返回值
        :param code: 0 is success, other is failure
        :param msg:
        :param result:
        :return:
        '''
        r = {}
        r['status'] = code
        r['msg'] = msg
        if result is not None:
            r['result'] = result
        return HttpResponse(json.dumps(r))

    def success_result(self, msg=None, result=None):
        if msg is None: msg = 'success'
        return self.get_result(code=0, msg=msg, result=result)

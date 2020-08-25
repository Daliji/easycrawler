/*
* 配置 js 文件
**/

_base_address = 'http://127.0.0.1:8000'; // 页面、接口、资源 访问基础地址

var config = {
    crawlerAddress: _base_address + '/crawlers', // 爬虫列表接口
    changeStateAddress: _base_address + '/change_state', // 切换爬虫状态接口
};
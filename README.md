# easycrawler

#### 介绍
python爬虫


#### 运行方式
直接执行`./runserver.sh`

启动之前记得修改：`crawler/settings.py/SERVICE_DATABASE` 为自己的Mysql数据库连接，如果需要用到ElasticSearch存储数据，记得修改 `crawler/settings.py/ES_URL`

#### 如何添加自己的爬虫
参考 `crawler/crawler/uestc_news` 爬虫自己写吧，写完以后记得在 `crawler/crawler/settings.py` 中注册自己的爬虫。
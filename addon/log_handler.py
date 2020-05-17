#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python+mitmproxy抓包过滤+redis消息订阅+websocket实时消息发送，日志实时输出到web界面
https://www.cnblogs.com/guanfuchang/p/6921336.html

运行命令: mitmdump -s log_handler.py
"""

import os
import time
import csv
import json
import requests
import urllib
import json
import logging
import redis
import datetime
from mitmproxy import http
from pytz import UTC
from dateutil.parser import parse
from influxdb import InfluxDBClient
from datetime import datetime
from elasticsearch import Elasticsearch
from datetime import datetime
from logzero import logger

es_index_name = 'logs_monitor_index'
es_server_host = '192.168.1.232'
es_server_port = 9200
url_list = ["test1-1.igetcool.com","test2-1.igetcool.com","igetcool-gateway-sim.igetcool.com","igetcool-gateway.igetcool.com"]


# redis连接池类，返回一个redis链接
class RedisPool:
    def __init__(self, host="192.168.1.237", port=8899, db=3):
        self.host = host
        self.port = port
        self.db = db

    def redis_connect(self):
        pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db)
        return redis.StrictRedis(connection_pool=pool)


pool = RedisPool("192.168.1.237", 8899, 3)
r = pool.redis_connect()

class  EsUntils():

    def __init__(self,index_name):
        self.es = Elasticsearch([{'host': es_server_host, 'port': es_server_port}])
        self.index_name = index_name


    def create_index(self):
        """
        创建索引
        :param index_name:
        :return:
        """
        if not self.index_name in self.es.indices.get("*"):
           self.es.indices.create(index=self.index_name)


    def insert(self,result):
        """
        插入数据
        :param result:
        :return:
        """
        self.es.index(index=self.index_name , doc_type="logs", body=result)
        logger.info('异步插入数据ES完成 ==>')



eu = EsUntils(es_index_name)


# 定义联运日志类型，根据抓包分析可知，类型可通过接口名获得
udpdcs_action_from_path = {
    'init_info': '初始化日志',
    'activity_open': '打开游戏日志',
    'activity_before_login': '登录界面前日志',
    'user_login': '登录日志',
    'enter_game': '进入游戏日志',
    'user_server_login': '选服日志',
    'user_create_role': '创角日志',
    'user_online': '在线日志',
    'role_level': '等级日志',
    'data.json': 'json格式',
}



def response(flow: http.HTTPFlow):
    """
    ly 日志处理
    :param flow:
    :return:
    """
    game_id, dict_msg = ly_log_filter(flow)
    # 日志保存与发布
    print('发布日志 = > {} - {}'.format(game_id,dict_msg))
    game_id = int(time.time())
    if game_id and dict_msg:
        eu.insert(dict_msg)


def ly_log_filter(flow):
    """
    联运日志处理
    根据域名，过滤大陆联运日志
    :param flow:
    :return:
    """
    host = flow.request.host
    method = flow.request.method
    url = urllib.parse.unquote(flow.request.url)
    dict_msg = None
    data_send = None
    game_id = None
    if host in url_list:
        plat = "大陆联运"
        status_code = flow.response.status_code
        ret = flow.response.content.decode('utf-8')
        try:
            ret = json.loads(ret)
        except Exception as e:
            logging.error(e)
        if method == "GET":
            # 从path中获取操作类型
            path = flow.request.path_components
            action_type = path[-1].rstrip(".php")
            # action_name = udpdcs_action_from_path.get(action_type)
            action_name = '代理日志'
            if action_name:
                # 从URL参数data中获取主要sdk请求数据
                querystring = flow.request._get_query()
                for eachp in querystring:
                    if eachp[0] == "data":
                        data = eachp[1]
                        try:
                            # 将关键的请求参数字符串转为字典，便于数据操作
                            """参数示例：{"eventId":"0","ip":"0","did":"863726035876487","appVersion":"1.2.3","sdkVersion":"3.1.4.0","platformId":"1","gameId":"1499130088511390","areaId":"0","serverId":"0","os":"android","osVersion":"6.0","device":"M5","deviceType":"android","screen":"1280*720","mno":"","nm":"WIFI","eventTime":"0","channel":"4399","channelOld":"4399","channelSy":"270","sim":"0","kts":"f409b38a02f14aafd1063d6bd30fa636","pkgName":"com.sy4399.xxtjd"}"""
                            data_send = json.loads(data)
                            game_id = data_send.get('gameId')
                        except Exception as e:
                            logging.error(e)

                dict_msg = {
                    "plat": plat,
                    "host": host,
                    "method": method,
                    "url": url,
                    "action_type": action_type,
                    "action_name": action_name,
                    "data": data_send,
                    "action_time": datetime.now().strftime(
                        '%Y-%m-%d %H:%M:%S.%f'),
                    "status_code": status_code,
                    "response": ret
                }
            else:
                logging.info("action_type=%s,操作类型为定义" % action_type)
        else:
            body = flow.request.content
            logging.info("使用了POST方式:%s" % url)
            logging.info("POST DATA:%s" % body)
            logging.info("*" * 200)
    return game_id, dict_msg


# 发布日志
def publish_log(game_id, dict_msg):
    print('发布日志 = >')
    if game_id:
        print("game_id:%s" % game_id)
        print("dict_msg:", dict_msg)
        if dict_msg:
            # 发布到redis频道game_id
            r.publish(game_id, json.dumps(dict_msg))
            # 保存到redis列表中，数据持久化
            key = str(game_id) + "_" + str(
                datetime.now().strftime("%Y%m%d"))
            r.lpush(key, json.dumps(dict_msg))




#!/usr/bin/python
# -*- coding: UTF-8 -*-


import csv
import time
import json
import requests
from elasticsearch import Elasticsearch
from datetime import datetime
from logzero import logger

es_index_name = 'logs_monitor_index'
es_server_host = '192.168.1.232'
es_server_port = 9200

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
        self.es.index(index=self.index_name , doc_type="api", body=result)
        logger.info('异步插入数据ES完成 ==>')








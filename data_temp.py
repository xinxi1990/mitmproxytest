#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
动态mock首页数据
'''

import time,json
now = time.strftime("%Y%m%d%H%M%S", time.localtime())

home_mock_url = "https://api.xueqiu.com/v4/statuses/public_timeline/categories.json"

def set_home_mock_data(value):
    home_mock_data = {
		"list": [{
			"category": 200,
			"column": "头条_" + str(value),
			"en": "recommend_v10_9"
		}, {
			"category": 6,
			"column": "直播",
			"en": "livenews"
		}, {
			"category": 105,
			"column": "沪深",
			"en": "cn"
		}, {
			"category": 115,
			"column": "科创板",
			"en": "tech_board"
		}, {
			"category": 102,
			"column": "港股1111",
			"en": "hk"
		}, {
			"category": 104,
			"column": "基金111",
			"en": "financial_management"
		}, {
			"category": 101,
			"column": "美股11",
			"en": "us"
		}, {
			"category": 111,
			"column": "房产",
			"en": "property"
		}, {
			"category": 113,
			"column": "私募",
			"en": "private_fund"
		}, {
			"category": 114,
			"column": "汽车",
			"en": "car"
		}, {
			"category": 110,
			"column": "保险",
			"en": "insurance"
		}]
	}
    return json.dumps(home_mock_data)




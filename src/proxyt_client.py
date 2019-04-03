#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
使用mitmproxy代理工具抓请求
"""

import mitmproxy.http
from mitmproxy import ctx
import json,time
from data_temp import home_mock_url,set_home_mock_data

is_mock = False

def request(flow: mitmproxy.http.HTTPFlow):
    request = flow.request
    if home_mock_url in request.pretty_url:
        print("=" * 50 + "拦截request开始" + "=" * 50)
        ctx.log.info("= 请求域名:{}=".format(request.host))
        ctx.log.info("=请求接口地址:{}=".format(request.pretty_url))
        ctx.log.info("=请求方法:{}=".format(request.method))
        ctx.log.warn("=请求body{}=".format("\n" + request.get_text()))
        print("=" * 50 + "拦截request结束" + "=" * 50)


def response(flow: mitmproxy.http.HTTPFlow):

    if home_mock_url in flow.request.url:
        ctx.log.info("=" * 50 + "拦截response开始" + "=" * 50)
        ctx.log.info(flow.request.url)
        response = flow.response
        now = time.strftime("%Y%m%d%H%M%S", time.localtime())
        get_mock_data = set_home_mock_data(now)
        ctx.log.info("=" * 50 + "mock数据" + "=" * 50)
        ctx.log.info(get_mock_data)
        ctx.log.info("=" * 50 + "mock数据" + "=" * 50)
        flow.response.set_text(get_mock_data)
        ctx.log.info("=响应header:{}=".format("\n" + str(response.headers)))
        ctx.log.info("=响应状态码:{}=".format("\n" + str(response.status_code)))
        ctx.log.info("=" * 50 + "拦截response结束" + "=" * 50)




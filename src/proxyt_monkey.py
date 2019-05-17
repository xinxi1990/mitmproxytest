#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
使用mitmproxy代理工具抓请求
"""

import mitmproxy.http
from mitmproxy import ctx
import json,time,os
is_mock = False

project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
now = time.strftime("%Y%m%d%H%M%S", time.localtime()) + "_url.log"
save_url_file = os.path.join(project_path, now)


def save_url(url):
    with open(save_url_file,"a") as f:
        f.write(url + "\n")


def request(flow: mitmproxy.http.HTTPFlow):
    request = flow.request
    print("=" * 50 + "拦截request开始" + "=" * 50)
    ctx.log.info("= 请求域名:{}=".format(request.host))
    ctx.log.info("=请求接口地址:{}=".format(request.pretty_url))
    ctx.log.info("=请求方法:{}=".format(request.method))
    ctx.log.warn("=请求body{}=".format("\n" + request.get_text()))
    print("=" * 50 + "拦截request结束" + "=" * 50)


def response(flow: mitmproxy.http.HTTPFlow):
    ctx.log.info("=" * 50 + "拦截response开始" + "=" * 50)
    ctx.log.info(flow.request.url)
    response = flow.response
    ctx.log.info("=响应header:{}=".format("\n" + str(response.headers)))
    ctx.log.info("=响应状态码:{}=".format("\n" + str(response.status_code)))
    save_url(flow.request.url + "," + str(response.status_code))
    ctx.log.info("=" * 50 + "拦截response结束" + "=" * 50)





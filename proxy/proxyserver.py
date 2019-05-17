#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
使用mitmproxy代理工具抓请求
"""

import mitmproxy.http
from mitmproxy import ctx
import json,time,os
from proxyrule import ProxyRule
from mathrandom import MathRandom


project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
now = time.strftime("%Y%m%d%H%M%S", time.localtime()) + "_url.log"
save_url_file = os.path.join(project_path, now)
black_list = ["png","jpg","jss","css"]


def save_url(url):
    with open(save_url_file,"a") as f:
        f.write(url + "\n")


def request(flow: mitmproxy.http.HTTPFlow):
    request = flow.request
    print("=" * 50 + "intercept request start" + "=" * 50)
    ctx.log.info("= host:{} =".format(request.host))
    ctx.log.info("= url:{} =".format(request.pretty_url))
    ctx.log.info("= method:{} =".format(request.method))
    ctx.log.warn("= body{} =".format("\n" + request.get_text()))
    print("=" * 50 + "拦截request结束" + "=" * 50)


def response(flow: mitmproxy.http.HTTPFlow):
    '''
    篡改response返回数据
    :param flow:
    :return:
    '''
    is_mock = False
    for balck_str in back_list:
        if balck_str in flow.request.url:
            ctx.log.info("=" * 50 + "not intercept response" + "=" * 50)
            break
        else:
            is_mock = True

    if int(response.status_code) == 200 and is_mock == True:
        original_data = (flow.response.text)
        if original_data.startswith("{") and original_data.endswith("}"):
            # save_url(original_data)
            # get_mock_data = ProxyRule(original_data).get_rule(MathRandom().PercentageRandom())
            get_mock_data = ProxyRule(original_data).get_defult_data()
            ctx.log.info("=" * 50 + "intercept response start" + "=" * 50)
            ctx.log.info("=" * 50 + "mock data" + "=" * 50)
            ctx.log.info(get_mock_data)
            ctx.log.info("=" * 50 + "mock data" + "=" * 50)
            flow.response.set_text(get_mock_data)
            ctx.log.info(flow.response.text)
            ctx.log.info("=" * 50 + "intercept response end" + "=" * 50)
    else:
        ctx.log.info("=" * 50 + "intercept response start" + "=" * 50)






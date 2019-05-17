#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
解析json数据
"""

from __future__ import print_function
from jsonpath_rw import jsonpath, parse
import json




def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                if len(value) == 0:
                    yield pre + [key, '{}']
                else:
                    for d in dict_generator(value, pre + [key]):
                        yield d
            elif isinstance(value, list):
                if len(value) == 0:
                    yield pre + [key, '[]']
                else:
                    for index,v in enumerate(value):
                        for d in dict_generator(v, pre + [key + "[{}]".format(index)]):
                            yield d
            elif isinstance(value, tuple):
                if len(value) == 0:
                    yield pre + [key, '()']
                else:
                    for v in value:
                        for d in dict_generator(v, pre + [key]):
                            yield d
            else:
                yield pre + [key, value]
    else:
        yield indict

if __name__ == "__main__":
    sJOSN =  {
                "base_config":{
                    "enforce":{
                        "value":"0",
                        "inherit":"0",
                        "global":"0"
                    },
                    "modify":{
                        "value":"0",
                        "inherit":"0",
                        "global":"0"
                    }
                },
                "safe_control_list":{
                    "list":[
                        {
                            "gid":"0",
                            "gname":"全网计算机",
                            "isactive":"1",
                            "rule_id":"0",
                            "rule_name":"请选择规则",
                            "time_range":"所有时间",
                            "time_range_id":"1",
                            "policy_tpl":"33",
                            "policy_tpl_id":"17",
                            "isonline":"3",
                            "priority":"88888"
                        },
                        {
                            "gid": "1",
                            "gname": "全网计算机",
                            "isactive": "1",
                            "rule_id": "0",
                            "rule_name": "请选择规则",
                            "time_range": "所有时间",
                            "time_range_id": "1",
                            "policy_tpl": "33",
                            "policy_tpl_id": "17",
                            "isonline": "3",
                            "priority": "99999"
                        }
                    ]
                }
            }


    # sValue = json.loads(sJOSN)
    for i in dict_generator(sJOSN):
        print('.'.join(i[0:-1]), ':', i[-1])
    jsonpath_expr = parse('safe_control_list.list[1].priority')
    print([match.value for match in jsonpath_expr.find(sJOSN)])

    # sValue = json.dumps(sJOSN)
    # httpjson1 = sValue.replace('base_config.enforce.value', "111111")
    # print(httpjson1)
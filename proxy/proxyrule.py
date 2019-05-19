#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
使用mitmproxy的rule的规则
@author:xinxi
"""

import json,time
from mathrandom import MathRandom
from parserjson import *
import random
import logger
logger.setup_logger('INFO')

class ProxyRule():

    def __init__(self,rep_json):
        self.rep_json = eval(rep_json)



    def get_defult_data(self):
        return  '{"h":{"c":0,"e":"","t":0.004232388,"s":1558015779},"c":{"data":{"status":1,"online_num":0,"reservation_num":0,"title":"直播测试22222","room_id":205,"intro":"test","starttime":1554972060,"starttime_desc":"周四16:41","duration":110,"endtime":1554978660,"id":205,"type":0,"log_id":205,"log_type":"igettv"}}}'


    def get_edit_data(self):
        json_path_list = get_jsonpath_list(self.rep_json)
        logger.log_info("{}".format(json_path_list))
        expr = MathRandom().get_random_list(json_path_list)
        logger.log_info("{}".format(expr))
        new_json_data = (edit_dict(expr=expr, new_value=self.get_random_string(), json_data=self.rep_json))
        logger.log_info("{}".format(new_json_data))
        return json.dumps(new_json_data)


    def save_replace_data(self):
        pass


    def not_intercept(self):
        '''
        不篡改请求,直接返回结果
        :return:
        '''
        logger.log_info("not_replace")
        return json.dumps(self.rep_json)


    def intercept_respones_json(self):
        '''
        对返回的json数据做随机做增删操作
        :return:
        '''
        print("replace_respones_json")
        pass




    def intercept_respones_str(self):
        '''
        对返回结果中的某个字段所增删改操作
        :return:
        '''
        print("replace_respones_str")
        pass


    def intercept_respones_list(self):
        '''
        多返回结果中的数组做增删改操作
        :return:
        '''
        print("replace_respones_list")
        pass



    def delay_respones_time(self):
        '''
        对返回数据做延迟返回
        :return:
        '''
        random_time = random.randint(100,1000)
        time.sleep(random_time/1000)
        logger.log_info("delay_respones_time:{}ms".format(random_time))



    @staticmethod
    def intercept_status_code():
        '''
        对返回的状态码做随机修改
        :return:
        '''
        code_list = [404,500,503,302,301]
        random_code = MathRandom().get_random_list(code_list)
        logger.log_info("replace_status_code:{}".format(random_code))
        return random_code



    def get_random_string(self):
        '''
        获取随机字符串
        :return:
        '''
        string_list = ['','超长字符串' * 100, self.special_string()]
        string = MathRandom().get_random_list(string_list)
        return string


    def special_string(self):
        '''
        特殊字符
        :return:
        '''
        list = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + [str(i) for i in range(10)] + ['.','-','~','_']
        # 大写字母+小写字母+数字 +特殊字符.-_~
        num = random.sample(list, 10)  # 输出10个固定长度的组合字符
        str1 = ''
        value = str1.join(num)  # 将取出的十个随机数进行重新合并
        logger.log_info("special_string is:{}".format(value))
        return value



    def get_random_event(self):
        '''
        获取随机事件
        :param num:
        :return:
        '''
        num = MathRandom().PercentageRandom()
        for case in switch(num):
            if case(0):
                self.not_intercept()
                break
            if case(1):
                self.intercept_respones_json()
                break
            if case(2):
                self.interceptrespones_str()
                break
            if case(3):
                self.intercept_respones_list()
                break
            if case(4):
                self.delay_respones_time()
                break
            if case(4):
                self.intercept_status_code()
                break
            if case():
               self.not_intercept()


class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False



if __name__ == '__main__':

    ProxyRule().get_rule(MathRandom().PercentageRandom())
#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
使用mitmproxy的rule的规则
"""

from mathrandom import MathRandom

class ProxyRule():

    def __init__(self,rep_json):
        self.rep_json = rep_json



    def get_defult_data(self):
        return  '{"h":{"c":0,"e":"","t":0.004232388,"s":1558015779},"c":{"data":{"status":1,"online_num":0,"reservation_num":0,"title":"直播测试22222","room_id":205,"intro":"test","starttime":1554972060,"starttime_desc":"周四16:41","duration":110,"endtime":1554978660,"id":205,"type":0,"log_id":205,"log_type":"igettv"}}}'


    def save_replace_data(self):
        pass


    def not_replace(self):
        print("not_replace")
        return self.rep_json

    def replace_respones_json(self):
        '''
        对返回的json数据做随机做增删操作
        :return:
        '''
        print("replace_respones_json")
        pass

    def replace_respones_str(self):
        '''
        对返回结果中的某个字段所增删改操作
        :return:
        '''
        print("replace_respones_str")
        pass


    def replace_respones_list(self):
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
        print("delay_respones_time")
        pass

    def replace_status_code(self):
        '''
        对返回的状态码做随机修改
        :return:
        '''
        print("replace_status_code")
        code_list = [404,500,503,302,301]



    def get_rule(self,num):

        for case in switch(num):
            if case(0):
                self.not_replace()
                break
            if case(1):
                self.replace_respones_json()
                break
            if case(2):
                self.replace_respones_str()
                break
            if case(3):
                self.replace_respones_list()
                break
            if case(4):
                self.delay_respones_time()
                break
            if case(4):
                self.replace_status_code()
                break
            if case():
               self.not_replace()


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
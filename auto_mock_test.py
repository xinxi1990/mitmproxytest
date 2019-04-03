#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest,os,subprocess
import time
from time import sleep
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


image_base64_list = []


class AutoMockTest(unittest.TestCase):

    loaded = False
    driver = None
    lanuch_time = 5

    def test_home_mock(self):
        print("setup")
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "192.168.56.101:5555"
        caps["appPackage"] = "com.xueqiu.android"
        caps["appActivity"] = ".view.WelcomeActivityAlias"
        caps["autoGrantPermissions"] = True
        caps["automationName"] = "UiAutomator2"
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        self.driver.implicitly_wait(6)
        if self.driver.find_elements_by_xpath("//*[@text='好的']"):
            self.driver.find_element_by_xpath("//*[@text='好的']").click()
        # current_path = os.path.abspath(os.path.dirname(__file__))
        # now = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".png"
        # file_path = os.path.join(current_path,now)
        # print("截图地址:" + file_path)
        # self.driver.get_screenshot_as_file(file_path)
        image_base64_list.append('<img src="data:image/png;base64,{}"/>'.format(self.driver.get_screenshot_as_base64()))


def kill_appium():
    '''
    结束appium进程
    :return:
    '''
    if os.popen('lsof -i:{}'.format(4723)).read() == '':
        print('appium pid is null')
    else:
        pid = os.popen('lsof -i:{}'.format(4723)).readlines()[1].split()[1]
        os.system('kill -9 {}'.format(pid))
        print('kill appium')


def start_appium():
    '''
    启动appium服务
    :return:
    '''
    kill_appium()
    args = 'appium --log {} --session-override'.format("appium.log")
    print('appium启动命令:{}'.format(args))
    appium = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, bufsize=1,close_fds=True)
    while True:
        appium_line = appium.stdout.readline().strip().decode()
        time.sleep(1)
        print("启动appium中...")
        if 'Welcome to Appium' in appium_line or 'Error: listen' in appium_line:
            print("appium启动成功")
            break


def kill_port(port):
    '''
    结束appium进程
    :return:
    '''
    if os.popen('lsof -i:{}'.format(port)).read() == '':
        print('pid is null')
    else:
        pid = os.popen('lsof -i:{}'.format(port)).readlines()[1].split()[1]
        os.system('kill -9 {}'.format(pid))
        print('kill port')


def gen_report_html(image_list):
    '''
    生成测试报告
    :return:
    '''
    image_str = ""
    for image in image_list:
        image_str +=image + "\n"
    html_tmp = """
        <html>
        <body>
        <h1>Auto Test Report</h1>
        {}
        </body>
        </html>
        """.format(image_str)
    current_path = os.path.abspath(os.path.dirname(__file__))
    now = time.strftime("%Y%m%d%H%M%S", time.localtime()) + "report.html"
    html_path = os.path.join(current_path,now)
    print(html_path)
    with open(html_path, "w", encoding='utf-8') as f:
        f.write(html_tmp)
        print("gen report over...")



if __name__ == '__main__':

    print("******************start_mock_test******************")
    current_path = os.path.abspath(os.path.dirname(__file__))
    proxy_path = os.path.join(current_path,"proxyt_client.py")
    print(proxy_path)
    # kill_port("8080")
    mock_cmd = "mitmdump -s {} > test.log".format(proxy_path)
    print(mock_cmd)
    subprocess.Popen(mock_cmd,shell=True)
    start_appium()
    test_suite = unittest.TestSuite()
    test_suite.addTest(AutoMockTest("test_home_mock"))
    test_suite.addTest(AutoMockTest("test_home_mock"))
    test_suite.addTest(AutoMockTest("test_home_mock"))
    # test_suite.addTest(AutoMockTest("test_home_mock"))
    # test_suite.addTest(AutoMockTest("test_home_mock"))
    runner = unittest.TextTestRunner()
    runner.run(test_suite)
    gen_report_html(image_base64_list)

    print("******************start_end_test******************")
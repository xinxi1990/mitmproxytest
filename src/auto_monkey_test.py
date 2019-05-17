#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest,os,subprocess



def run_moneky():

    cmd = "java -jar /Users/xinxi/PycharmProjects/mitmproxytest/monkey/AndroidMonkey-1.0.jar " \
          "-f /Users/xinxi/PycharmProjects/mitmproxytest/monkey_report " \
          "-u 192.168.56.101:5555 " \
          "-p 4723 -b 4724 -t 30 " \
          "-a /Users/xinxi/Downloads/app_release_6.1.0_20190423101533.apk " \
          "-m xinxi@luojilab.com " \
          "-v release"
    subprocess.Popen(cmd, shell=True)



if __name__ == '__main__':

    print("******************start_mock_test******************")
    current_path = os.path.abspath(os.path.dirname(__file__))
    proxy_path = os.path.join(current_path,"proxyt_monkey.py")
    print(proxy_path)
    # kill_port("8080")
    mock_cmd = "mitmdump -s {} > test.log".format(proxy_path)
    print(mock_cmd)
    subprocess.Popen(mock_cmd,shell=True)
    run_moneky()
    print("******************start_end_test******************")
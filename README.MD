# 介绍

使用mitproxy代理工具做Android自动化Mock数据测试


# 环境搭建

## 创建虚拟环境(python 3.7)
```angularjs
python3.7 -m venv /Users/xinxi/PycharmProjects/mitmproxytest/venv or virtualenv venv

 

deactivate
```

## 安装mitmproxy
```angular2html
pip install mitmproxy
```

## 安装appium client
```angular2html
pip install appium_python_client
```

## 安装appium server
```angular2html
npm install appium
```

## Android设备

使用Android6.0系统,大于6.0系统无法抓https包

# 使用

## 手机连接代理
移动设备和电脑保存在一个wifi网络下,在移动设备在网络代理填写电脑ip+8080(端口)

![image](images/proxy.png)

## mitproxy https证书安装
```
在浏览器输入:mitm.it,选择Android证书下载并安装
```
![image](images/mitm.png)

## 脚本运行

```
cd src;python auto_mock_test.py
```


## 开启代理工具
```
mitmdump -s proxyt_client.py (没有gui模式)
```

```
mitmweb -s proxyt_client.py (启动web页面模式)
```

```
mitmweb -s proxyserver.py (启动web页面模式)
```


# 报告
![image](images/report.png)


# 相关参考

借助 anyproxy 二次开发，改善统计打点日志测试流程<br>
https://testerhome.com/topics/9271

mitmproxy<br>
https://github.com/mitmproxy/mitmproxy.git<br>

mitmproxy使用<br>
https://blog.csdn.net/NN375701364/article/details/82151332



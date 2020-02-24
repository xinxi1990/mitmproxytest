# 介绍

使用mitproxy代理工具做Android自动化Mock数据测试

# 规则
```
随机对请求数据做随机拦截篡改,支持事件如下:
1.随机对返回value做修改/删除
2.随机对返回list做删除 （可能会引起客户端崩溃,慎用）
3.随机对返回接口状态码修改
4.随机对返回接口时间做延迟修改
```

## 安装

```angular2html
pip3.7 install mitmproxy
```


## 使用

执行mock数据
```angularjs
mitmdump -s proxyserver.py
```

生成报告
```angularjs
参数1:需要保存的报告地址
参数2:保存到本地篡改数据地址
python genhtml.py ~/PycharmProjects/mitmproxytest/proxy ~/PycharmProjects/mitmproxytest/proxy/20190521143711_intercept.log
```

# 展示

![image](报告1.jpg)

![image](报告2.jpg)


## 抓包WebSocket 
```angular2html
mitmdump -s snifferWS.py --verbose
```
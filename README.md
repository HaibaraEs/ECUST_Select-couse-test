﻿# 选课系统状态检测
用于检测华东理工大学研究生教育管理系统（http://graduate.ecust.edu.cn/webui/login.aspx） 选课平台（又称薛定谔的选课平台）是否开放

本项目解决了选课平台开放时间不确定导致的同学们错过选课最佳时机的问题。
运行本项目后，当选课平台开放时，会向指定邮箱发送提醒邮件。与此同时，为了防止邮件被忽视，还会以系统最大音量播放Deja Vu,以方便各位老司机选课。

依赖：
bs4
smtplib
win32api

注意：需要自行修改邮箱、SMTP授权码及自己的学号密码

做了一点微小的工作，谢谢大家！

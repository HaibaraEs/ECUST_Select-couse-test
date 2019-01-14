# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib
import time


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


class Crawling:
    # public data
    originURL = 'http://graduate.ecust.edu.cn/WebUI/'
    originHeaders = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
        'Connection': 'keep-alive'}  # 记录headers, 伪装成浏览器访问. 'referer'的值要依据网页添加
    session = None  # 一个会话, 让cookie得以保存传递. 后面都使用这个session进行post和get

    # personal data
    __originData = {'Button1': ''}  # 登录时要提交的数据: 用户名, 密码, '__VIEWSTATE'的值要从登录页源码中提取

    def __init__(self, userName, passward):
        self.__originData['username'] = userName
        self.__originData['password'] = passward
        self.__originData['btnlogin'] = '登录(Login)'
        self.session = requests.session()

    def setLoginData(self, URL, headers):
        data = self.__originData
        data['__VIEWSTATE'] = BeautifulSoup(self.session.get(URL, headers=headers).text, 'lxml').findAll('input')[
            0].get('value')  # 解析得到'__VIEWSTATE'的值, 将'__VIEWDATE'的值加入字典

        return data

    def setHeaders(self, refererURL):
        headers = self.originHeaders
        headers['Referer'] = refererURL
        return headers

    def login(self):
        loginPageURL = self.originURL + 'login.aspx'  # 登录的网址(post请求网址, 同时也是referer网址)

        loginHeaders = self.setHeaders(loginPageURL)  # 得到post需要的headers
        loginData = self.setLoginData(loginPageURL, loginHeaders)  # 得到post需要的data
        homePage = self.session.post(loginPageURL, data=loginData, headers=loginHeaders)  # 发出post请求(登录), 进入个人教务系统主页
        return homePage

    def switchToSelect(self):
        homePageURL = self.originURL + 'left.aspx?id=83'  # 主页网址(referer网址)
        selectPageURL = self.originURL + 'Student/SelectFirst.aspx'  # 得到课表页数据来源网址(get请求网址)
        selectPageHeaders = self.setHeaders(homePageURL)  # 得到get需要的headers
        selectPage = self.session.get(selectPageURL, headers=selectPageHeaders)  # 发出get请求,得到课表页数据

        return selectPage


if __name__ == '__main__':
    while True:
        userName = '改成你的学号'
        passward = '改成你的密码'
        # 登录
        spider = Crawling(userName, passward)
        homePage = spider.login()
        selectPage = spider.switchToSelect()
        if selectPage.text != '<br><br><p align=center><font color=red> 现在没有进行网上选课！</font></p>':
            # 邮箱
            form_addr = '这里改成发件人的qq邮箱地址'
            # 不是邮箱密码,而是开启SMTP服务时的授权码
            password = '这里改成你的SMTP授权码'
            # 收件人的邮箱
            to_addr = '这里改成收件人的qq邮箱地址，可以和发件人相同'
            # qq邮箱的服务器地址
            smpt_server = 'smtp.qq.com'

            # 设置邮件信息
            msg = MIMEText(selectPage.text, 'plain', 'utf-8')
            msg['From'] = _format_addr('选课侦查员 <%s>' % form_addr)
            msg['To'] = _format_addr('学生 <%s>' % to_addr)
            msg['Subject'] = Header('选课开始！', charset='utf-8').encode()

            # 发送邮件
            server = smtplib.SMTP(smpt_server, port=25)
            server.set_debuglevel(1)
            server.login(form_addr, password)
            server.sendmail(form_addr, [to_addr], msg.as_string())
            server.quit()
            print('选课开始')
            import PlayDejavu

            PlayDejavu.PlayDejavu()
            break
        print('现在没有进行网上选课！')
        time.sleep(60)

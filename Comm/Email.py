# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:Email.py
@time:2021/04/19
@describe：发送邮件
"""
import smtplib
import os
import logging
from Comm.log import log_init
from Conf.config import smtp_cfg, email_cfg
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

log_init()
logger = logging.getLogger('Mario.email')

# 文件大小限制20M
file_size = 20
# 文件大小限制10个
file_count = 10


class Email:

    def __init__(self, subject, context=None, attachment=None):
        '''
        构造函数
        :param subject:邮件标题
        :param context:邮件正文
        :param attachment:邮件附件
        '''
        self.subject = subject
        self.context = context
        self.attachment = attachment
        # 发送带附件的邮件，首先要创建MIMEMultipart()实例，然后构造附件，如果有多个附件，可依次构造，最后利用smtplib.smtp发送。
        self.message = MIMEMultipart()
        self.message_init()

    def message_init(self):
        '''
        邮件内容处理
        :return:
        '''
        # 邮件标题
        if self.subject:
            self.message['Subject'] = Header(self.subject, 'utf-8')
        else:
            raise ValueError("无效的标题：{}，请输入正确的标题！".format(self.subject))
            logger.error("无效的标题：{}，请输入正确的标题！".format(self.subject))
        # 邮件发件人
        self.message['Form'] = email_cfg['sender']
        # 邮件收件人
        self.message['To'] = email_cfg['receivers']
        # 邮件正文内容
        if self.context:
            self.message.attach(MIMEText(self.context, 'html', 'utf-8'))
        # 邮箱附件
        if self.attachment:
            # isinstance() 函数来判断一个对象是否是一个已知的类型;判断是否为单个文件
            if isinstance(self.attachment, str):
                self.attach_handle(self.attachment)
            # 判断是否为多个文件
            if isinstance(self.attachment, list):
                count = 0
                # 循环多个文件
                for each in self.attachment:
                    # 判断文件数量是否等于小于预设值
                    if count <= file_count:
                        self.attach_handle(each)
                        count += 1
                    else:
                        logger.warning("附件数量超过预设值：{}个".format(file_count))
                        break

    def attach_handle(self, file):
        '''
        附件处理
        :param file:附件
        :return:
        '''
        # 判断是否为文件并且大小是否符合预设值
        if os.path.isfile(file) and os.path.getsize(file) <= file_size * 1024 * 1024:
            attach = MIMEApplication(open(file, 'rb').read())
            attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            attach["Content-Type"] = 'application/octet-stream'
            self.message.attach(attach)
        else:
            logger.error('附件超过{0}M，或者{1}不存在'.format(file_size, file))

    def send_mail(self):
        '''
        发送邮件
        :return:发送结果
        '''
        # 创建邮件发送连接(smtp有两个端口号：465.587)
        conn = smtplib.SMTP_SSL(smtp_cfg['host'], int(smtp_cfg['port']))
        logger.info("连接邮箱成功～host:{0},port:{1}".format(smtp_cfg['host'], smtp_cfg['port']))
        # 邮件发送结果变量
        result = True
        try:
            # 登陆邮件
            conn.login(smtp_cfg['user'], smtp_cfg['password'])
            logger.info('登陆邮箱成功～  登陆用户名：{}'.format(smtp_cfg['user']))
            conn.sendmail(email_cfg['sender'], email_cfg['receivers'], self.message.as_string())
            logger.info("获取发件人信息成功：{0},获取收件人成功:{1}".format(email_cfg['sender'], email_cfg['receivers']))
        except smtplib.SMTPAuthenticationError:
            result = False
            logger.error("登陆邮箱失败～请检查账号密码是否正确！", exc_info=True)
        except smtplib.SMTPException:
            result = False
            logger.error("发送邮件失败！", exc_info=True)
        finally:
            conn.close()
            logger.info('关闭邮箱连接～')
        return result

# https://www.baidu.com/s?ie=UTF-8&wd=BeautifulReport
# 自动化测试报告
# BeautifulReport

# mail = Email('测试组第三周周报','第一次发送')
# send = mail.send_mail()
# print(send)

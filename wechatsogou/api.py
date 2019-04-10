# -*- coding: utf-8 -*-

import binascii
import codecs
import logging
import os
import random
import re
import time
import urllib

import httplib2
import requests
from bs4 import BeautifulSoup
from lxml import etree

from .basic import WechatSogouBasic
from .exceptions import *

logger = logging.getLogger()

requests.packages.urllib3.disable_warnings()


class WechatSogouApi(WechatSogouBasic):
    """基于搜狗搜索的的微信公众号爬虫接口  接口类
    """

    def __init__(self, **kwargs):
        super(WechatSogouApi, self).__init__(**kwargs)

    def get_k_h(self, url, text):
        """计算k和h"""
        k = 0
        h = 0
        try:
            k = random.randrange(1, 100)
            normal = re.findall(r'a\+4\+parseInt\("(.*?)"', text, re.S)[0]
            h = url[34 + int(normal) + k]
        except:
            logger.exception("Exception Logged")
        return str(k), h

    def search_gzh_info(self, name, page=1):
        """搜索公众号

        Args:
            name: 搜索关键字
            page: 搜索的页数

        Returns:
            列表，每一项均是{'name':name,'wechatid':wechatid,'jieshao':jieshao,'renzhen':renzhen,'qrcode':qrcodes,'img':img,'url':url}
            name: 公众号名称
            wechatid: 公众号id
            jieshao: 介绍
            renzhen: 认证，为空表示未认证
            qrcode: 二维码 暂无
            img: 头像图片
            url: 文章地址
            last_url: 最后一篇文章地址 暂无
        """
        html_text, request_url = self._search_gzh_text(name, page)

        try:
            page = etree.HTML(html_text)
        except:
            logger.exception("Exception Logged")
            return ""

        img = list()
        # 头像
        info_imgs = page.xpath(u"//div[@class='img-box']//img")
        for info_img in info_imgs:
            img.append(info_img.attrib['src'])
        # 文章列表
        url = list()
        info_urls = page.xpath(u"//div[@class='img-box']//a")
        for info_url in info_urls:
            url_temp = info_url.attrib['href']
            realurl = ""
            if "https" not in url_temp:
                url_temp = "https://weixin.sogou.com" + url_temp
            try:
                # 计算加密k
                k, h = self.get_k_h(url_temp, html_text)
                url_temp = "%s&k=%s&h=%s" % (url_temp, k, h)
                # 转成正式的文章列表url
                text = self._get(url_temp, referer=request_url)  # 需要优化
                arr = text.split("url +=")
                for iterating_var in arr:
                    realurl += iterating_var.split("'")[1]
            except WechatSogouVcodeException:
                logger.exception("Exception Logged")
                realurl = ""

            url.append(realurl)

        # 微信号
        wechatid = page.xpath(u"//label[@name='em_weixinhao']/text()")

        # 公众号名称
        name = list()
        name_list = page.xpath(u"//div[@class='txt-box']/p/a")
        for name_item in name_list:
            name.append(name_item.xpath('string(.)'))

        # 二维码
        qrcode = list()
        qrcode_list = page.xpath(u"//span[@class='pop']//img[1]/@src")
        for qrcode_item in qrcode_list:
            qrcode.append(urllib.parse.unquote(qrcode_item.split("&url=")[1]))

        last_url = list()
        jieshao = list()
        renzhen = list()
        list_index = 0
        # 介绍、认证、最近文章
        info_instructions = page.xpath(u"//ul[@class='news-list2']/li")
        for info_instruction in info_instructions:
            cache = self._get_elem_text(info_instruction)
            cache = cache.replace('red_beg', '').replace('red_end', '')
            cache_list = cache.split('\n')
            cache_re = re.split(u'功能介绍：|认证：|最近文章：', cache_list[0])
            if cache.find("最近文章") == -1:
                last_url.insert(list_index, "")
            list_index += 1

            if len(cache_re) > 1:
                jieshao.append(re.sub(r"document.write\(authname\('[0-9]'\)\)", "", cache_re[1]))
                if "authname" in cache_re[1]:
                    renzhen.append(cache_re[2])
                else:
                    renzhen.append('')
            else:
                # 没取到，都为空吧
                jieshao.append('')
                renzhen.append('')

        returns = list()
        for i in range(len(name)):
            returns.append(
                {
                    'name': name[i],
                    'wechatid': wechatid[i],
                    'jieshao': jieshao[i],
                    'renzhen': renzhen[i],
                    'qrcode': qrcode[i],
                    'img': img[i],
                    'url': url[i],
                    'last_url': ''
                }
            )
        return returns

    def get_gzh_info(self, wechatid):
        """获取公众号微信号wechatid的信息

        因为wechatid唯一确定，所以第一个就是要搜索的公众号

        Args:
            wechatid: 公众号id

        Returns:
            字典{'name':name,'wechatid':wechatid,'jieshao':jieshao,'renzhen':renzhen,'qrcode':qrcodes,'img':img,'url':url}
            name: 公众号名称
            wechatid: 公众号id
            jieshao: 介绍
            renzhen: 认证，为空表示未认证
            qrcode: 二维码
            img: 头像图片
            url: 最近文章地址
        """
        try:
            info = self.search_gzh_info(wechatid, 1)
            return info[0] if info else ""
        except:
            logger.exception("Exception Logged")
            return ""

    def get_gzh_message(self, **kwargs):
        """解析最近文章页  或  解析历史消息记录

        Args:
            ::param url 最近文章地址
            ::param wechatid 微信号
            ::param wechat_name 微信昵称(不推荐，因为不唯一)

            最保险的做法是提供url或者wechatid

        Returns:
            gzh_messages 是 列表，每一项均是字典，一定含有字段qunfa_id,datetime,type
            当type不同时，含有不同的字段，具体见文档
        """
        url = kwargs.get('url', None)
        wechatid = kwargs.get('wechatid', None)
        wechat_name = kwargs.get('wechat_name', None)
        if url:
            text = self._get_gzh_article_by_url_text(url)
        elif wechatid:
            gzh_info = self.get_gzh_info(wechatid)
            url = gzh_info['url']
            text = self._get_gzh_article_by_url_text(url)
        elif wechat_name:
            gzh_info = self.get_gzh_info(wechat_name)
            url = gzh_info['url']
            text = self._get_gzh_article_by_url_text(url)
        else:
            # raise WechatSogouException('get_gzh_message need param text and url')
            return '链接已过期'

        if u'链接已过期' in text:
            return '链接已过期'
        return self._deal_gzh_article_dict(self._get_gzh_article_by_url_dict(text))

    def deal_article_content(self, **kwargs):
        """获取文章内容

        Args:
            ::param url 文章页 url
            ::param text 文章页 文本

        Returns:
            content_html, content_rich, content_text
            content_html: 原始文章内容，包括html标签及样式
            content_rich: 包含图片（包括图片应展示的样式）的文章内容
            content_text: 包含图片（`<img src="..." />`格式）的文章内容
        """
        url = kwargs.get('url', None)
        text = kwargs.get('text', None)
        if text:
            pass
        elif url:
            text = self._get_gzh_article_text(url)
        else:
            raise WechatSogouException('deal_article_content need param url or text')

        # 纯文字
        bs_obj = BeautifulSoup(text, features="lxml")
        content_text = bs_obj.find("div", {"class": "rich_media_content", "id": "js_content"})
        if not content_text:  # 分享的文章
            content_text = bs_obj.find("div", {"class": "share_media", "id": "js_share_content"})

        content_html = ""
        if content_text:
            content_html = content_text.get_text()

        return content_html

    # 下载文章到本地
    def down_html(self, url, dir_name):
        try:
            url = url.replace('\\x26', '&')
            url = url.replace('x26', '&')
            print(u'正在下载文章：' + url)

            h = httplib2.Http(timeout=30)
            html = self._get_gzh_article_text(url)
            content = html

            # 正则表达式javascript里的获取相关变量
            tmp = re.findall('var ct = "(.*?)";', content)
            if tmp:
                ct = tmp[0]
            else:
                ct = ""
            msg_cdn_url = re.findall('var msg_cdn_url = "(.*?)";', content)[0]
            nickname = re.findall('var nickname = "(.*?)";', content)[0]
            if nickname == "":
                nickname = "not has name"
            if ct == "":
                ct = time.time()

            ctime = time.strftime("%Y%m%d%H%M%S", time.localtime(int(ct)))  # int将字符串转成数字，不区分int和long, 这里将时间秒数转成日期格式
            # 建立文件夹
            # 编码转换
            # if isinstance(dir_name, str):
            #     dir_name = dir_name.encode('GB18030', 'ignore')
            # else:
            #     dir_name = dir_name.decode('utf-8', 'ignore').encode('GB18030', 'ignore')
            #
            # if isinstance(nickname, str):
            #     nickname = nickname.encode('GB18030', 'ignore')
            # else:
            #     if chardet.detect(nickname)['encoding'] == 'KOI8-R':
            #         print("KOI8")
            #         nickname = nickname.decode('KOI8-R', 'ignore').encode('GB18030', 'ignore')
            #     else:
            #         print("GB18030")
            #         nickname = nickname.decode('utf-8', 'ignore').encode('GB18030', 'ignore')

            my_dir = 'WeiXinGZH/' + nickname + '/' + ctime + '/' + dir_name + '/'
            # my_dir = my_dir.decode('gb2312', 'ignore')
            my_dir = my_dir.replace("?", "")
            my_dir = my_dir.replace("\\", "")
            my_dir = my_dir.replace("*", "")
            my_dir = my_dir.replace(":", "")
            my_dir = my_dir.replace('\"', "")
            my_dir = my_dir.replace("<", "")
            my_dir = my_dir.replace(">", "")
            my_dir = my_dir.replace("|", "")

            try:
                os.makedirs(my_dir)  # 建立相应的文件夹

            except:
                # 不处理
                pass

            # 下载封面
            url = msg_cdn_url
            resp, contentface = h.request(url)

            file_name = my_dir + 'cover.jpg'
            codecs.open(file_name, mode='wb').write(contentface)

            # 下载其他图片
            soup = BeautifulSoup(content, 'html.parser')
            count = 0
            err_count = 0
            for link in soup.find_all('img'):
                try:
                    err_count += 1
                    if err_count > 200:
                        break  # 防止陷阱

                    if link.get('data-src') is not None:
                        count = count + 1
                        orurl = link.get('data-src')
                        url = orurl.split('?')[0]  # 重新构造url，原来的url有一部分无法下载
                        resp, content = h.request(url)

                        matchurlvalue = re.search(r'wx_fmt=(?P<wx_fmt>[^&]*)', orurl)  # 无参数的可能是gif，也有可能是jpg
                        if matchurlvalue is not None:
                            wx_fmt = matchurlvalue.group('wx_fmt')  # 优先通过wx_fmt参数的值判断文件类型
                            if '?' in wx_fmt:
                                wx_fmt = wx_fmt.split('?')[0]
                        else:
                            wx_fmt = binascii.b2a_hex(content[0:4])  # 读取前4字节转化为16进制字符串

                        phototype = {'jpeg': '.jpg', 'gif': '.gif', 'png': '.png', 'jpg': '.jpg', b'47494638': '.gif',
                                     b'ffd8ffe0': '.jpg', b'ffd8ffe1': '.jpg', b'ffd8ffdb': '.jpg', b'ffd8fffe': '.jpg',
                                     'other': '.jpg', b'89504e47': '.png'}  # 方便写文件格式
                        file_name = 'Picture' + str(count) + phototype[wx_fmt]
                        file_path = my_dir + file_name
                        open(file_path, 'wb').write(content)

                        # 图片替换成本地地址
                        re_url = 'data-src="%s(.+?)"' % (url[:-5])
                        re_pic = 'src="%s"' % file_name
                        html = re.sub(re_url, re_pic, html)
                except:
                    logger.exception("Exception Logged")
                    continue

            with open("%sindex.html" % my_dir, "wb") as code:
                code.write(html.encode('utf-8'))

            print(u'文章下载完成')
            ret_path = os.path.abspath('.')
            ret_path = ret_path.replace('\\', "/")
            ret_path = "%s/%sindex.html" % (ret_path, my_dir)
        except WechatSogouHistoryMsgException:
            print(u'文章内容有异常编码，无法下载')
            return ""
        return ret_path

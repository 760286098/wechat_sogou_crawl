# -*- coding: utf-8 -*-

import http.cookiejar as cookie
import random
import re
import time
import traceback
import urllib
import urllib.parse

import requests
from bs4 import BeautifulSoup
from lxml import etree

from . import config
from .chaojiying import Chaojiying_Client
from .exceptions import *


class WechatSogouApi:
    """基于搜狗搜索的的微信公众号爬虫接口  接口类
    """

    def __init__(self, **kwargs):
        self._session = requests.session()
        if config.cjy_name != '' and config.cjy_pswd != '':
            self._ocr = Chaojiying_Client(config.cjy_name, config.cjy_pswd, '31ae38ecbf750bc16a24dd78206f5499')

        self._agents = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        ]

    @staticmethod
    def get_k_h(url, text):
        """计算k和h"""
        k = random.randrange(1, 100)
        normal = re.findall(r'a\+4\+parseInt\("(.*?)"', text, re.S)[0]
        h = url[34 + int(normal) + k]
        return str(k), h

    @staticmethod
    def _get_elem_text(elem):
        """抽取lxml.etree库中elem对象中文字
        """
        rc = []
        for node in elem.itertext():
            rc.append(node.strip())
        return ''.join(rc)

    def search_gzh_info(self, keyword):
        """搜索公众号
        """
        request_url = 'https://weixin.sogou.com/weixin?type=1&query=' + urllib.parse.quote(keyword)
        text = self._get_by_unlock(request_url, unlock_platform=self._unlock_sogou, host='weixin.sogou.com').text
        page = etree.HTML(text)

        img = page.xpath(u"//div[@class='img-box']//img")[0].attrib['src'][2:]  # 头像图片
        url = ""  # 文章地址
        url_temp = "https://weixin.sogou.com" + page.xpath(u"//div[@class='img-box']//a")[0].attrib['href']
        try:
            k, h = self.get_k_h(url_temp, text)
            url_temp = "%s&k=%s&h=%s" % (url_temp, k, h)
            # 转成正式的文章列表url
            text = self._get(url_temp, referer=request_url).text
            # text = self._get_by_unlock(url_temp, unlock_platform=self._unlock_sogou, host='weixin.sogou.com',
            #                            referer=request_url).text
            arr = text.split("url +=")
            for iterating_var in arr:
                url += iterating_var.split("'")[1]
        except Exception:
            traceback.print_exc()
            url = ""

        wechatid = page.xpath(u"//label[@name='em_weixinhao']/text()")[0]  # 微信号
        keyword = page.xpath(u"//div[@class='txt-box']/p/a")[0].xpath('string(.)')  # 公众号名称
        qrcode = urllib.parse.unquote(page.xpath(u"//span[@class='pop']//img[1]/@src")[0].split("&url=")[1])  # 二维码
        jieshao = ''  # 介绍
        renzhen = ''  # 认证
        recent = ''  # 最近文章
        recent_time = ''  # 最近发表时间
        for elem in page.xpath("//ul[@class='news-list2']/li[1]//dl"):
            text = self._get_elem_text(elem).replace('red_beg', '').replace('red_end', '')
            if '功能介绍：' in text:
                jieshao = text.split('功能介绍：')[-1]
                continue
            if '认证：' in text:
                renzhen = text.split('认证：')[-1]
                continue
            if '最近文章：' in text:
                recent = text.split('最近文章：')[-1].split('document')[0]
                recent_time = re.findall(r'document\.write\(timeConvert\(\'(.*?)\'\)\)', text, re.S)[0]

        if recent_time:
            recent_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(recent_time)))

        result = {
            'name': keyword,
            'wechatid': wechatid,
            'jieshao': jieshao,
            'renzhen': renzhen,
            'qrcode': qrcode,
            'img': img,
            'url': url,
            'recent': recent,
            'recent_time': recent_time
        }
        return result

    def get_gzh_message(self, url):
        """解析最近文章页  或  解析历史消息记录
        """
        if url:
            text = self._get_by_unlock(url, unlock_platform=self._unlock_wechat, host='mp.weixin.qq.com').text
            if u'链接已过期' not in text:
                return self._deal_gzh_article_dict(self._get_gzh_article_by_url_dict(text))
        return '链接已过期'

    def deal_article_content(self, url):
        """获取文章内容
        """
        text = self._get(url, host='mp.weixin.qq.com').text
        bs_obj = BeautifulSoup(text, features="lxml")
        content_text = bs_obj.find("div", {"class": "rich_media_content", "id": "js_content"})
        if not content_text:
            content_text = bs_obj.find("div", {"class": "share_media", "id": "js_share_content"})
        if content_text:
            return content_text.get_text()
        return ""

    def _get(self, url, **kwargs):
        referer = kwargs.get('referer', None)
        host = kwargs.get('host', None)
        if host:
            del kwargs['host']
        if referer:
            del kwargs['referer']
        headers = {
            "Host": host if host else 'weixin.sogou.com',
            "Upgrade-Insecure-Requests": '1',
            "User-Agent": random.choice(self._agents),
            "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            "Referer": referer if referer else 'https://weixin.sogou.com/',
            "Accept-Encoding": 'gzip, deflate, br',
            "Accept-Language": 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'
        }
        r = self._session.get(url, headers=headers, **kwargs)
        if not r.ok:
            raise WechatSogouRequestsException('WechatSogouAPI get error', r)
        r.encoding = 'utf-8'
        return r

    def _unlock_sogou(self, url):
        self._session.headers.update(
            {'referer': 'https://weixin.sogou.com/antispider/?from=' + urllib.parse.quote(url)})
        r_captcha = self._session.get(
            'http://weixin.sogou.com/antispider/util/seccode.php?tc={}'.format(int(round(time.time() * 1000))))
        if not r_captcha.ok:
            raise WechatSogouRequestsException('WechatSogouAPI get img', r_captcha)

        unlock_url = 'http://weixin.sogou.com/antispider/thank.php'
        data = {
            'c': self._identify_image(r_captcha.content),
            'r': urllib.parse.quote(url),
            'v': 5
        }
        headers = {
            'User-Agent': random.choice(self._agents),
            'Host': 'weixin.sogou.com',
            'Referer': 'http://weixin.sogou.com/antispider/?from=%2f' + urllib.parse.quote(
                url.replace('https://', ''))
        }
        r_unlock = self._session.post(unlock_url, data, headers=headers)
        r_unlock.encoding = 'utf-8'
        if not r_unlock.ok:
            raise WechatSogouVcodeOcrException(
                'unlock[{}] failed: {}'.format(unlock_url, r_unlock.text, r_unlock.status_code))

        remsg = eval(r_unlock.content)
        if remsg['code'] != 0:
            self._ocr.report_error(self.__pic_id)
            raise WechatSogouVcodeOcrException(
                '[WechatSogouAPI identify image] code: {code}, msg: {msg}'.format(code=remsg.get('code'),
                                                                                  msg=remsg.get('msg')))
        # 搜狗又增加验证码机制
        cookie_jar = cookie.MozillaCookieJar()
        cookie_jar.set_cookie(
            cookie.Cookie(version=0, name='SNUID', value=remsg['id'], port=None, port_specified=False,
                          domain='sogou.com', domain_specified=False, domain_initial_dot=False, path='/',
                          path_specified=True, secure=None, expires=None, discard=True, comment=None,
                          comment_url=None, rest={'HttpOnly': None}, rfc2109=False))
        self._session.cookies.update(cookie_jar)

        pb_url = 'http://pb.sogou.com/pv.gif?uigs_productid=webapp&type=antispider&subtype=0_seccodeInputSuccess' \
                 '&domain=weixin&suv=%s&snuid=%s&t=%s' % (
                     '', remsg['id'], str(time.time())[0:10])
        headers = {
            'User-Agent': random.choice(self._agents),
            'Host': 'pb.sogou.com',
            'Referer': 'http://weixin.sogou.com/antispider/?from=%2f' + urllib.parse.quote(
                url.replace('https://', ''))
        }
        self._session.get(pb_url, headers=headers)

    def _unlock_wechat(self, url):
        r_captcha = self._session.get('https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(time.time() * 1000))
        if not r_captcha.ok:
            raise WechatSogouRequestsException('WechatSogouAPI get img', r_captcha)

        unlock_url = 'https://mp.weixin.qq.com/mp/verifycode'
        data = {
            'cert': time.time() * 1000,
            'input': self._identify_image(r_captcha.content)
        }
        headers = {
            'Host': 'mp.weixin.qq.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': url
        }
        r_unlock = self._session.post(unlock_url, data, headers=headers)
        if not r_unlock.ok:
            raise WechatSogouVcodeOcrException(
                'unlock[{}] failed: {}[{}]'.format(unlock_url, r_unlock.text, r_unlock.status_code))

        remsg = eval(r_unlock.content)
        if remsg['ret'] != 0:
            self._ocr.report_error(self.__pic_id)
            raise WechatSogouVcodeOcrException(
                '[WechatSogouAPI identify image] code: {ret}, msg: {errmsg}, cookie_count: {cookie_count}'.format(
                    ret=remsg.get('ret'), errmsg=remsg.get('errmsg'), cookie_count=remsg.get('cookie_count')))

    def _identify_image(self, content):
        print(u"出现验证码，准备自动识别")
        if hasattr(self, '_ocr'):
            for i in range(3):
                result = self._ocr.create(content, 1902)
                self.__pic_id = result['pic_id']
                if result['err_str'] != 'OK':
                    print(u"超级鹰识别失败，错误为：%s 更换验证码再次尝试，尝试次数：%d" % (result['err_str'], i))
                    self._ocr.report_error(self.__pic_id)
                    time.sleep(1)
                    continue
                else:
                    img_code = result['pic_str']
                    print(u"验证码识别成功 验证码：%s" % img_code)
                    return img_code

    def _get_by_unlock(self, url, unlock_platform, host, referer=None):
        if referer:
            r = self._get(url, referer=referer, host=host)
        else:
            r = self._get(url, host=host)
        if 'antispider' in r.url or '请输入验证码' in r.text:
            for i in range(3):
                try:
                    unlock_platform(url=url)
                    break
                except WechatSogouVcodeOcrException as e:
                    traceback.print_exc()
                    if i == 2:
                        raise WechatSogouVcodeOcrException(e)

            r = self._get(url, referer='https://weixin.sogou.com/antispider/?from=%2f' + urllib.parse.quote(
                url.replace('https://', '')), host=host)
        return r

    @staticmethod
    def _get_gzh_article_by_url_dict(text):
        """最近文章页 文章信息
        """
        try:
            msglist = re.findall("var msgList = (.+?)};", text, re.S)[0]
            msglist = msglist + '}'

            html = msglist
            html = html.replace('&#39;', '\'')
            html = html.replace('&amp;', '&')
            html = html.replace('&gt;', '>')
            html = html.replace('&lt;', '<')
            html = html.replace('&yen;', '¥')
            html = html.replace('amp;', '')
            html = html.replace('&lt;', '<')
            html = html.replace('&gt;', '>')
            html = html.replace('&nbsp;', ' ')
            html = html.replace('\\', '')

            msgdict = eval(html)
            return msgdict
        except Exception:
            traceback.print_exc()
            return ''

    @staticmethod
    def _deal_gzh_article_dict(msgdict, **kwargs):
        """解析 公众号 群发消息
        """
        biz = kwargs.get('biz', '')
        uin = kwargs.get('uin', '')
        key = kwargs.get('key', '')
        items = list()
        for listdic in msgdict['list']:
            item = dict()
            comm_msg_info = listdic['comm_msg_info']
            item['qunfa_id'] = comm_msg_info.get('id', '')  # 不可判重，一次群发的消息的id是一样的
            item['datetime'] = comm_msg_info.get('datetime', '')
            item['type'] = str(comm_msg_info.get('type', ''))
            if item['type'] == '1':
                # 文字
                item['content'] = comm_msg_info.get('content', '')
            elif item['type'] == '3':
                # 图片
                item[
                    'img_url'] = 'https://mp.weixin.qq.com/mp/getmediadata?__biz=' + \
                                 biz + '&type=img&mode=small&msgid=' + \
                                 str(item['qunfa_id']) + '&uin=' + uin + '&key=' + key
            elif item['type'] == '34':
                # 音频
                item['play_length'] = listdic['voice_msg_ext_info'].get('play_length', '')
                item['fileid'] = listdic['voice_msg_ext_info'].get('fileid', '')
                item['audio_src'] = 'https://mp.weixin.qq.com/mp/getmediadata?__biz=' + biz + '&type=voice&msgid=' + \
                                    str(item['qunfa_id']) + '&uin=' + uin + '&key=' + key
            elif item['type'] == '49':
                # 图文
                app_msg_ext_info = listdic['app_msg_ext_info']
                url = app_msg_ext_info.get('content_url')
                if url:
                    url = 'http://mp.weixin.qq.com' + url if 'http://mp.weixin.qq.com' not in url else url
                else:
                    url = ''
                msg_index = 1
                item['main'] = msg_index
                item['title'] = app_msg_ext_info.get('title', '')
                item['digest'] = app_msg_ext_info.get('digest', '')
                item['fileid'] = app_msg_ext_info.get('fileid', '')
                item['content_url'] = url
                item['source_url'] = app_msg_ext_info.get('source_url', '')
                item['cover'] = app_msg_ext_info.get('cover', '')
                item['author'] = app_msg_ext_info.get('author', '')
                item['copyright_stat'] = app_msg_ext_info.get('copyright_stat', '')
                items.append(item)
                if app_msg_ext_info.get('is_multi', 0) == 1:
                    for multidic in app_msg_ext_info['multi_app_msg_item_list']:
                        url = multidic.get('content_url')
                        if url:
                            url = 'http://mp.weixin.qq.com' + url if 'http://mp.weixin.qq.com' not in url else url
                        else:
                            url = ''
                        itemnew = dict()
                        itemnew['qunfa_id'] = item['qunfa_id']
                        itemnew['datetime'] = item['datetime']
                        itemnew['type'] = item['type']
                        msg_index += 1
                        itemnew['main'] = msg_index
                        itemnew['title'] = multidic.get('title', '')
                        itemnew['digest'] = multidic.get('digest', '')
                        itemnew['fileid'] = multidic.get('fileid', '')
                        itemnew['content_url'] = url
                        itemnew['source_url'] = multidic.get('source_url', '')
                        itemnew['cover'] = multidic.get('cover', '')
                        itemnew['author'] = multidic.get('author', '')
                        itemnew['copyright_stat'] = multidic.get('copyright_stat', '')
                        items.append(itemnew)
                continue
            elif item['type'] == '62':
                item['cdn_videoid'] = listdic['video_msg_ext_info'].get('cdn_videoid', '')
                item['thumb'] = listdic['video_msg_ext_info'].get('thumb', '')
                item['video_src'] = 'https://mp.weixin.qq.com/mp/getcdnvideourl?__biz=' + biz + '&cdn_videoid=' + item[
                    'cdn_videoid'] + '&thumb=' + item['thumb'] + '&uin=' + uin + '&key=' + key
            items.append(item)
        return items

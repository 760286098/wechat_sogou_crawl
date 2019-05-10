# -*- coding: utf-8 -*-

import time
import traceback

from wechatsogou import *

wechats = WechatSogouApi()
mysql = mysql('mp_info')

mp_list = mysql.find(0, order_sql=" order by _id")
for mp_item in mp_list:
    try:
        # 查看一下该号今天是否已经发送文章
        last_qunfa_id = mp_item['last_qunfa_id']
        cur_qunfa_id = last_qunfa_id
        wz_url = mp_item['wz_url']
        print(mp_item['name'])
        # 获取最近文章信息
        wz_list = wechats.get_gzh_message(url=wz_url)
        if u'链接已过期' in wz_list:
            wechat_info = wechats.search_gzh_info(mp_item['wx_hao'])
            if 'url' not in wechat_info:
                continue
            wz_url = wechat_info['url']
            wz_list = wechats.get_gzh_message(url=wz_url)
            mysql.table('mp_info').where({'_id': mp_item['_id']}).update(
                {'wz_url': wechat_info['url'], 'logo_url': wechat_info['img'], 'qr_url': wechat_info['qrcode'],
                 'recent_wz': wechat_info['recent'],
                 'recent_time': wechat_info['recent_time'], })
        for wz_item in wz_list:
            temp_qunfa_id = int(wz_item['qunfa_id'])
            if last_qunfa_id >= temp_qunfa_id:
                print(u"没有更新文章")
                break
            if cur_qunfa_id < temp_qunfa_id:
                cur_qunfa_id = temp_qunfa_id
            if wz_item['type'] == '49':
                if not wz_item['content_url']:
                    continue

                mysql.table('wenzhang_info').add({'title': wz_item['title'],
                                                  'source_url': wz_item['source_url'],
                                                  'cover_url': wz_item['cover'],
                                                  'description': wz_item['digest'],
                                                  'date_time': time.strftime("%Y-%m-%d %H:%M:%S",
                                                                             time.localtime(wz_item['datetime'])),
                                                  'mp_id': mp_item['_id'],
                                                  'content_url': wz_item['content_url'],
                                                  'author': wz_item['author'],
                                                  'qunfa_id': wz_item['qunfa_id'],
                                                  'msg_index': wz_item['main'],
                                                  'content': wechats.deal_article_content(url=wz_item['content_url'])})
        # 更新最新推送ID
        if last_qunfa_id < cur_qunfa_id:
            mysql.table('mp_info').where({'_id': mp_item['_id']}).update(
                {'last_qunfa_id': cur_qunfa_id,
                 'update_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))})
    except Exception:
        traceback.print_exc()
        continue
print('success')

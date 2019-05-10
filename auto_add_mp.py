# -*- coding: utf-8 -*-

import time
import traceback

from wechatsogou import *

wechats = WechatSogouApi()
mysql = mysql('add_mp_list')

add_list = mysql.find(0)
for add_item in add_list:
    try:
        print("add by: %s" % add_item)
        if not mysql.table('mp_info').where({'name': add_item['name']}).find(1):
            wechat_info = wechats.search_gzh_info(add_item['name'])
            if wechat_info != "":
                mysql.table('mp_info').add({'name': wechat_info['name'],
                                            'wx_hao': wechat_info['wechatid'],
                                            'description': wechat_info['jieshao'],
                                            'company': wechat_info['renzhen'],
                                            'logo_url': wechat_info['img'],
                                            'qr_url': wechat_info['qrcode'],
                                            'wz_url': wechat_info['url'],
                                            'recent_wz': wechat_info['recent'],
                                            'recent_time': wechat_info['recent_time'],
                                            'last_qunfa_id': 0,
                                            'create_time': time.strftime("%Y-%m-%d %H:%M:%S",
                                                                         time.localtime(time.time()))})
        else:
            print(u"已经存在的公众号")
        mysql.table('add_mp_list').where({'_id': add_item['_id']}).delete()  # 删除已添加项
    except Exception:
        traceback.print_exc()
        continue
print("success")

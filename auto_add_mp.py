# -*- coding: utf-8 -*-

import time
import traceback
from sys import argv

from wechatsogou import *

wechats = WechatSogouApi()
mysql = mysql('mp_info')

for i in range(1, len(argv)):
    try:
        print("添加公众号： " + argv[i])
        if not mysql.where({'name': argv[i]}).find(1):
            wechat_info = wechats.search_gzh_info(argv[i])
            if wechat_info != "":
                mysql.add({'name': wechat_info['name'],
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
            print(u"已经存在的公众号: " + argv[i])
    except Exception:
        traceback.print_exc()
        continue
print("success")

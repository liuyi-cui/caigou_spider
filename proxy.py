import random
import time

import requests


class SingleTon:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(SingleTon, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance


class IpData(SingleTon):  # 同一时间只允许存在一个代理对象
    url = ""  # 代理接口
    ipdata = {}  # 当url count为1的时候，存入该属性
    ipdatas = []  # 当url count大于1的时候，存入该属性

    def load_ipdata(self):  # 当前ip为空的时候，从网上获取ip.
        try:
            response = requests.get(self.url)
            proxy = response.json()
            ipdatas = proxy['msg']
            if len(ipdatas) == 1:
                self.ipdata = ipdatas[0]
            elif len(ipdatas) > 1 and not isinstance(ipdatas, str):
                self.ipdatas = ipdatas
            else:  # {'code': '3001', 'msg': 提取频繁请按照规定频率提取！'}
                print(ipdatas)
                time.sleep(3)
                self.load_ipdata()
        except Exception as e:
            print(f'网站获取代理ip失败：{e}')

    def update_ipdata(self, msg):  # ip过期时，清除ip
        if msg == self.ipdata:
            self.ipdata = {}
        if msg in self.ipdatas:
            self.ipdatas.remove(msg)

    def get_ipdata(self):  # 获取ip
        if self.ipdata == {} and self.ipdatas == []:
            self.load_ipdata()
        if self.ipdata != {}:
            return self.ipdata
        else:
            return random.choice(self.ipdatas)

    def origin_ipdata(self):
        self.ipdata = {}
        self.ipdatas = []

    def get_proxy(self, msg):  # msg格式为{'port': '44613', 'ip': '112.113.154.75'}
        try:
            ipdata = msg['ip'] + ':' + msg['port']
            proxies = {'http': ipdata, 'https': ipdata}
            return proxies
        except Exception as e:
            print(f'获取代理失败: <{msg}>:<{e}>')





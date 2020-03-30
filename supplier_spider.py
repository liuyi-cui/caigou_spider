# 爬取供应商数据

base_url = "http://www.ccgp-guangdong.gov.cn"
url = "http://www.ccgp-guangdong.gov.cn/organization/querySellerOrgList.do"  # 广东省政府采购供应商名录
headers = {
    'Connection': 'close',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
}

import datetime

import requests
from lxml import etree

from proxy import IpData
from dateutils import trans_date_str


def get_response(url, proxies, form_data, ipdata, msg, trynum=0):
    if trynum == 10:  # 连续更换10次ip均出错
        return None
    try:
        response = requests.post(url=url, data=form_data, headers=headers, proxies=proxies,
                                 timeout=20)
        if response.status_code == 200:
            return response
        elif response.status_code == 404:
            ipdata.update_ipdata(msg)  # 删除当前ip
            msg = ipdata.get_ipdata()
            proxies = ipdata.get_proxy(msg)
            trynum += 1
            return get_response(url, proxies, form_data, ipdata, msg, trynum=trynum)
        else:
            fail_time = datetime.datetime.now()
            fail_time = trans_date_str(fail_time)
            with open('failed_url.txt', 'a', encoding='utf-8')as f:
                f.write(f'{fail_time}:<{url}>: 该网站获取失败: <{response.status_code}>\n')
            return None
    except requests.exceptions.ProxyError:  # 代理ip被拒绝访问
        ipdata.update_ipdata(msg)  # 删除当前ip
        msg = ipdata.get_ipdata()
        proxies = ipdata.get_proxy(msg)
        trynum += 1
        return get_response(url, proxies, form_data, ipdata, msg, trynum=trynum)
    except requests.exceptions.Timeout:
        ipdata.update_ipdata(msg)  # 删除当前ip
        msg = ipdata.get_ipdata()
        proxies = ipdata.get_proxy(msg)
        trynum += 1
        return get_response(url, proxies, form_data, ipdata, msg, trynum=trynum)
    except Exception as e:
        print(f'爬取页面错误 <{url}>: <{e}>')
        ipdata.update_ipdata(msg)  # 删除当前ip
        msg = ipdata.get_ipdata()
        proxies = ipdata.get_proxy(msg)
        trynum += 1
        return get_response(url, proxies, form_data, ipdata, msg, trynum=trynum)


def max_page_spider():
    ipdata = IpData()
    msg = ipdata.get_ipdata()
    proxies = ipdata.get_proxy(msg)
    form_data = {
        'pointPageIndexId': '1',
        'pageIndex': '1',  # 从首页获取最大页数
        'pageSize': '10',
    }
    headers['Content-Length'] = str(len(form_data))
    response = get_response(url, proxies, form_data, ipdata, msg, trynum=0)
    if response:  # 解析获取最大页数
        selector = etree.HTML(response.text, )
    else:
        print('获取首页数据失败')








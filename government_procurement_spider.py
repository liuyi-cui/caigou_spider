# 各个省市的采购供应商，代理机构，违法失信名单
import datetime
import time
import json

import requests
from lxml import etree

from proxy import IpData
from dateutils import trans_date_str

headers = {
    'Connection': 'close',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
    "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
}


def get_response_post(url, headers, proxies, form_data, ipdata, msg, trynum=0):
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
            if trynum == 10:
                fail_time = datetime.datetime.now()
                fail_time = trans_date_str(fail_time)
                with open('failed_url.txt', 'a', encoding='utf-8')as f:
                    f.write(f'{fail_time}:<{url}>: 该网站获取失败: <{response.status_code}>\n')
                return None
            return get_response_post(url, headers, proxies, form_data, ipdata, msg, trynum=trynum)
        elif response.status_code == 502 or response.status_code == 411:
            ipdata.update_ipdata(msg)  # 删除当前ip
            msg = ipdata.get_ipdata()
            proxies = ipdata.get_proxy(msg)
            trynum += 1
            if trynum == 10:
                fail_time = datetime.datetime.now()
                fail_time = trans_date_str(fail_time)
                with open('failed_url.txt', 'a', encoding='utf-8')as f:
                    f.write(f'{fail_time}:<{url}>: 该网站获取失败: <{response.status_code}>\n')
                return None
            return get_response_post(url, headers, proxies, form_data, ipdata, msg, trynum=trynum)
        else:
            ipdata.update_ipdata(msg)  # 删除当前ip
            msg = ipdata.get_ipdata()
            proxies = ipdata.get_proxy(msg)
            trynum += 1
            if trynum == 10:
                fail_time = datetime.datetime.now()
                fail_time = trans_date_str(fail_time)
                with open('failed_url.txt', 'a', encoding='utf-8')as f:
                    f.write(f'{fail_time}:<{url}>: 该网站获取失败: <{response.status_code}>\n')
                return None
            return get_response_post(url, headers, proxies, form_data, ipdata, msg, trynum=trynum)
    except requests.exceptions.ProxyError:  # 代理ip被拒绝访问
        ipdata.update_ipdata(msg)  # 删除当前ip
        msg = ipdata.get_ipdata()
        proxies = ipdata.get_proxy(msg)
        trynum += 1
        return get_response_post(url, headers, proxies, form_data, ipdata, msg, trynum=trynum)
    except requests.exceptions.Timeout:
        ipdata.update_ipdata(msg)  # 删除当前ip
        msg = ipdata.get_ipdata()
        proxies = ipdata.get_proxy(msg)
        trynum += 1
        return get_response_post(url, headers, proxies, form_data, ipdata, msg, trynum=trynum)
    except Exception as e:
        print(f'爬取页面错误 <{url}>: <{e}>')
        ipdata.update_ipdata(msg)  # 删除当前ip
        msg = ipdata.get_ipdata()
        proxies = ipdata.get_proxy(msg)
        trynum += 1
        return get_response_post(url, headers, proxies, form_data, ipdata, msg, trynum=trynum)


def get_response_get(url, headers, proxies, ipdata, msg, trynum=0):

    try:
        response = requests.get(url=url, headers=headers, proxies=proxies, timeout=10,
                                allow_redirects=False)
        if response.status_code == 200:
            return response
        elif response.status_code == 404:
            ipdata.update_ipdata(msg)  # 删除当前ip
            msg = ipdata.get_ipdata()
            proxies = ipdata.get_proxy(msg)
            trynum += 1
            if trynum == 10:
                fail_time = datetime.datetime.now()
                fail_time = trans_date_str(fail_time)
                with open('failed_url.txt', 'a', encoding='utf-8')as f:
                    f.write(f'{fail_time}:<{url}>: 该网站获取失败: <{response.status_code}>\n')
                return None
            return get_response_get(url, headers, proxies, ipdata, msg, trynum=trynum)
        elif response.status_code == 502 or response.status_code == 411:
            ipdata.update_ipdata(msg)  # 删除当前ip
            msg = ipdata.get_ipdata()
            proxies = ipdata.get_proxy(msg)
            trynum += 1
            if trynum == 10:
                fail_time = datetime.datetime.now()
                fail_time = trans_date_str(fail_time)
                with open('failed_url.txt', 'a', encoding='utf-8')as f:
                    f.write(f'{fail_time}:<{url}>: 该网站获取失败: <{response.status_code}>\n')
                return None
            return get_response_get(url, headers, proxies, ipdata, msg, trynum=trynum)
        else:
            ipdata.update_ipdata(msg)  # 删除当前ip
            msg = ipdata.get_ipdata()
            proxies = ipdata.get_proxy(msg)
            trynum += 1
            if trynum == 10:
                fail_time = datetime.datetime.now()
                fail_time = trans_date_str(fail_time)
                with open('failed_url.txt', 'a', encoding='utf-8')as f:
                    f.write(f'{fail_time}:<{url}>: 该网站获取失败: <{response.status_code}>\n')
                return None
            return get_response_get(url, headers, proxies, ipdata, msg, trynum=trynum)
    except requests.exceptions.ProxyError:  # 代理ip被拒绝访问
        ipdata.update_ipdata(msg)  # 删除当前ip
        msg = ipdata.get_ipdata()
        proxies = ipdata.get_proxy(msg)
        trynum += 1
        return get_response_get(url, headers, proxies, ipdata, msg, trynum=trynum)
    except requests.exceptions.Timeout:
        ipdata.update_ipdata(msg)  # 删除当前ip
        msg = ipdata.get_ipdata()
        proxies = ipdata.get_proxy(msg)
        trynum += 1
        return get_response_get(url, headers, proxies, ipdata, msg, trynum=trynum)
    except Exception as e:
        print(f'爬取页面错误 <{url}>: <{e}>')
        ipdata.update_ipdata(msg)  # 删除当前ip
        msg = ipdata.get_ipdata()
        proxies = ipdata.get_proxy(msg)
        trynum += 1
        return get_response_get(url, headers, proxies, ipdata, msg, trynum=trynum)


class GuangDongSpider:
    base_url = 'http://www.ccgp-guangdong.gov.cn'
    supplier_url = 'http://www.ccgp-guangdong.gov.cn/organization/querySellerOrgList.do'  # 广东省政府采购供应商名录
    agency_url = 'http://www.ccgp-guangdong.gov.cn/organization/queryPerformOrgList.do'  # 代理商名录
    break_promise_url = 'http://www.ccgp-guangdong.gov.cn/queryIllegalList.html'


    def get_max_page(self, url, proxies, form_data, ipdata, msg):
        # headers['Content-Length'] = str(len(form_data))
        response = get_response_post(url, headers, proxies, form_data, ipdata, msg, trynum=0)
        if response:  # 解析获取最大页数
            selector = etree.HTML(response.text, etree.HTMLParser())
            pages = selector.xpath("//a[@class='aborder']/span[@class='aspan']")
            if len(pages) > 0:
                max_page = int(pages[-1].xpath('text()')[0])
            else:
                print('没有获取到最大页数')
                max_page = 0
            return max_page
        else:
            print('获取首页数据失败')
            time.sleep(10)
            return self.get_max_page(url, proxies, form_data, ipdata, msg)  # 失败再重新获取


    def get_suppliers(self):

        def get_supplier_info(childresponse):  # 供应商详情页获取信息
            childselector = etree.HTML(childresponse.text, etree.HTMLParser())
            try:
                tr_eleselector = childselector.xpath('/html/body/div[2]/table/tbody/tr')
                def get_dict(tr):  # 针对详细页面的一行，获取相应信息
                    name = tr.xpath('th')
                    if name != []:
                        for i in range(len(name)):
                            name = name[i].xpath('text()')[0].strip()
                            value = tr.xpath('td/text()')[i].strip()
                            return {name: value}
                    else:
                        return None

                supplier_info = list(map(get_dict, tr_eleselector))
                return supplier_info
            except Exception as e:
                fail_time = datetime.datetime.now()
                fail_time = trans_date_str(fail_time)
                with open('failed_url.txt', 'a', encoding='utf-8')as f:
                    f.write(f'{fail_time}:<{childresponse.request.url}>: 该网站解析xpath: <{e}>\n')
                return None

        ipdata = IpData()
        msg = ipdata.get_ipdata()
        proxies = ipdata.get_proxy(msg)
        form_data = {
            'pointPageIndexId': '1',
            'pageIndex': '1',  # 从首页获取最大页数
            'pageSize': '10',
        }
        max_page = self.get_max_page(self.supplier_url, proxies, form_data, ipdata, msg)
        headers['referer'] = 'http://www.ccgp-guangdong.gov.cn/organization/querySellerOrgList.do'
        headers['cookie'] = 'Ks8ae9gdPofpF0yrRJi1UrDsaM-hm8uARsgRyaj46O9l8dsmqJyJ!-1509577578'
        for page in range(178, max_page+1):  # 从1循环到最大页数
            print('供应商第{}页'.format(page))
            form_data['pageIndex'] = page
            # headers['Content-Length'] = str(len(form_data))
            response = get_response_post(self.supplier_url, headers, proxies, form_data, ipdata, msg, trynum=0)
            if response:  # 解析供应商详情地址
                selector = etree.HTML(response.text, etree.HTMLParser())
                childurls = selector.xpath('//div[@class="m_m_cont"]//tr/td[3]/a')
                real_childurls = []
                for childurl in childurls:
                    childurl = self.base_url + childurl.xpath('@href')[0]
                    if childurl not in real_childurls:
                        real_childurls.append(childurl)
                        childresponse = get_response_get(childurl, headers, proxies, ipdata, msg)
                        if childresponse:
                            print('详情页：', childurl)
                            try:
                                supplier_info = get_supplier_info(childresponse)
                                supplier_info.append({'url_source': childurl})
                                with open('government_procurement/guangdong/supplier.txt', 'a', encoding='utf-8')as f:
                                    f.write(json.dumps(supplier_info, ensure_ascii=False))
                                    f.write(',')
                            except Exception as e:
                                fail_time = datetime.datetime.now()
                                fail_time = trans_date_str(fail_time)
                                with open('failed_url.txt', 'a', encoding='utf-8')as f:
                                    f.write(f'{fail_time}:<{childresponse.request.url}>: 该网站解析xpath: <{e}>\n')

                        else:
                            print('详情页信息获取失败')
                        time.sleep(3)
                    else:
                        continue

    def get_agency(self):

        def get_agency_info(childresponse):  # 供应商详情页获取信息
            childselector = etree.HTML(childresponse.text, etree.HTMLParser())
            tr_eleselector = childselector.xpath('/html/body/div[2]/table[1]/tbody/tr')
            def get_dict(tr):  # 针对详细页面的一行，获取相应信息
                name = tr.xpath('th')
                if name != []:
                    for i in range(len(name)):
                        name = name[i].xpath('text()')[0].strip()
                        value = tr.xpath('td/text()')[i].strip()
                        return {name: value}
                else:
                    return None
            if tr_eleselector:
                supplier_info = list(map(get_dict, tr_eleselector))
                return supplier_info
            else:
                print(childresponse.request.url, '该代理页面数据提取失败')

        ipdata = IpData()
        msg = ipdata.get_ipdata()
        proxies = ipdata.get_proxy(msg)
        form_data = {
            'pointPageIndexId': '1',
            'pageIndex': '1',  # 从首页获取最大页数
            'pageSize': '10',
        }
        # max_page = self.get_max_page(self.agency_url, proxies, form_data, ipdata, msg)
        headers['referer'] = 'http://www.ccgp-guangdong.gov.cn/organization/queryPerformOrgList.do'
        # headers['cookie'] = 'Ks8ae9gdPofpF0yrRJi1UrDsaM-hm8uARsgRyaj46O9l8dsmqJyJ!-1509577578'
        headers['cookie'] = 'hlce-4C6jnLFpch9x2dUya_0eBJR--2owaXh62fo9E2FQRFQfWrf!-1509577578'
        # for page in range(19, max_page+1):
        for page in range(28, 114):
            print('代理第{}页'.format(page))
            form_data['pageIndex'] = page
            # headers['Content-Length'] = str(len(form_data))
            response = get_response_post(self.agency_url, headers, proxies, form_data, ipdata, msg, trynum=0)
            print('列表页：', form_data)
            if response:  # 解析代理商详情地址
                selector = etree.HTML(response.text, etree.HTMLParser())
                childurls = selector.xpath('//td[@align="center"]/a')
                unduplicate_childurls = []
                for childurl in childurls:
                    childurl = self.base_url + childurl.xpath('@href')[0]
                    if childurl not in unduplicate_childurls:
                        unduplicate_childurls.append(childurl)
                        childresponse = get_response_get(childurl, headers, proxies, ipdata, msg)
                        print('详情页：', childurl)
                        if childresponse:
                            try:
                                supplier_info = get_agency_info(childresponse)
                                supplier_info.append({'url_source': childurl})
                                with open('government_procurement/guangdong/agency.txt', 'a', encoding='utf-8')as f:
                                    f.write(json.dumps(supplier_info, ensure_ascii=False))
                                    f.write(',')
                            except Exception as e:
                                fail_time = datetime.datetime.now()
                                fail_time = trans_date_str(fail_time)
                                with open('failed_url.txt', 'a', encoding='utf-8')as f:
                                    f.write(f'{fail_time}:<{childresponse.request.url}>: 该网站获取失败: <{response.status_code}>\n')
                            finally:
                                time.sleep(3)
                        else:
                            print('详情页信息获取失败')
                            time.sleep(3)
                    else:
                        continue

            else:
                print('代理商地址解析失败')
                continue


    def get_broken_pormise(self):
        ipdata = IpData()
        msg = ipdata.get_ipdata()
        proxies = ipdata.get_proxy(msg)
        response = get_response_get(self.break_promise_url, headers, proxies, ipdata, msg)
        if response:
            selector = etree.HTML(response.text, etree.HTMLParser())
            tr_ele = selector.xpath("//div[@id='contianer']/div[@class='m_m_cont']/table/tr")
            values = []
            titles = []
            for i in tr_ele:
                title = i.xpath('th')
                if title != []:
                    titles = [j.xpath('text()')[0] for j in title]
                else:
                    value = [j.xpath('text()')[0].strip() for j in i.xpath('td')]
                    values.append(value)
            with open('government_procurement/guangdong/broken_promise.txt', 'a', encoding='utf-8')as f:
                f.write(json.dumps(titles, ensure_ascii=False))
                f.write('\n')
                f.write(json.dumps(values, ensure_ascii=False))
        else:
            print('失信首页获取失败')



if __name__ == "__main__":
    guangdongspider = GuangDongSpider()
    print('start')
    # guangdongspider.get_broken_pormise()
    # print('失信名单获取完毕')
    # guangdongspider.get_agency()
    # print('代理商获取完毕')
    guangdongspider.get_suppliers()
    print('供应商获取完毕')

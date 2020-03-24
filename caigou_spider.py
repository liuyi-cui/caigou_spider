import datetime
import re
import time

import requests
from lxml import etree

from aijiengine import OriginBid, OriginBidInfo, OriginBidText, TFileAttach, RProjBid
from dateutils import trans_date_str
from proxy import IpData


source = 'CCGP'  # 数据来源-中国政府采购网
operator = 'liuyi'
base_url = "http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index={}&timeType={}"
file_base_url = "http://www.ccgp.gov.cn"  # 附件的baseurl
uuid_url = "https://www.aijitech.com/smartbid/genuid"  # 获取bid_id
web_encoding = "ISO-8859-1"
headers = {
    'Connection': 'close',
    "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
}


def get_uuid():  # 根据接口获取uuid
    try:
        response = requests.get(url=uuid_url, headers=headers, timeout=20)
        uuid = response.text
        return uuid
    except Exception as e:
        print(f'获取uuid失败：<{e}>')
        return None


def _format_r_projbid(proj_bid_list):
    '''
    格式化r_proj_bid是数据
    :param proj_bid_list:
    :return:
    '''
    def _format_r(proj_bid):
        return (0, proj_bid[0], proj_bid[1], 1, proj_bid[2], proj_bid[3])  # id, proj_id, bid_id, is_valid, create_time, create_by
    return tuple(map(_format_r, proj_bid_list))


def _format_bid_info(bid_info_dict, bid_id, info_addr, create_time):
    """
    组装origin_bid_info表数据
    :param bid_info_dict:
    :param bid_id:
    :param info_addr: 数据来源 LIST OR ABSTRACT
    :param create_time:
    :return:
    """

    def format_dict(bid_info_dict_key):
        return (0, bid_id, bid_info_dict_key, bid_info_dict[bid_info_dict_key], info_addr, '1', '0',
                create_time, operator)
    return list(map(format_dict, bid_info_dict))


def _format_file_attach(file_attach_list, create_time, operator):
    '''
    格式化t_file_attach数据
    :param file_attach_list:
    :param create_time:
    :param operator:
    :return:
    '''
    def _format_file_data(file_attach_info):
        return (0, file_attach_info[2], file_attach_info[3], file_attach_info[4], file_attach_info[0],
                file_attach_info[1], 1, create_time, operator)

    return tuple(map(_format_file_data, file_attach_list))


def get_response(url, proxies, ipdata, msg, trynum=0):
    if trynum == 10:  # 连续更换10次ip均出错
        return None
    try:
        response = requests.get(url=url, headers=headers, proxies=proxies, timeout=20,
                                allow_redirects=False)
        if response.status_code == 200:
            return response
        elif response.status_code == 404:
            ipdata.update_ipdata(msg)  # 删除当前ip
            msg = ipdata.get_ipdata()
            proxies = ipdata.get_proxy(msg)
            trynum += 1
            return get_response(url, proxies, ipdata, msg, trynum=trynum)
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
        return get_response(url, proxies, ipdata, msg, trynum=trynum)
    except requests.exceptions.Timeout:
        ipdata.update_ipdata(msg)  # 删除当前ip
        msg = ipdata.get_ipdata()
        proxies = ipdata.get_proxy(msg)
        trynum += 1
        return get_response(url, proxies, ipdata, msg, trynum=trynum)
    except Exception as e:
        print(f'爬取页面错误 <{url}>: <{e}>')
        ipdata.update_ipdata(msg)  # 删除当前ip
        msg = ipdata.get_ipdata()
        proxies = ipdata.get_proxy(msg)
        trynum += 1
        return get_response(url, proxies, ipdata, msg, trynum=trynum)


def get_detail_url(base_url, page_num):  # 获取指定页数中的公告url
    page_index = (i for i in range(1, page_num+1))
    timeType = 0  # {0: '今日', 1: '近三日', 2: '近一周', 3: '近一月', 4: '近半年'}
    ipdata = IpData()
    msg = ipdata.get_ipdata()
    proxies = ipdata.get_proxy(msg)
    def deal_list_page(response):
        create_time = datetime.datetime.now()
        create_time = trans_date_str(create_time)
        info_addr = 'LIST'
        selector = etree.HTML(response.text, etree.HTMLParser())
        url_list_href = selector.xpath('//ul[@class="vT-srch-result-list-bid"]/li/a')
        ori_list_href = selector.xpath('//ul[@class="vT-srch-result-list-bid"]/li/span')
        proj_bid_list = []
        origin_bid_data = []  # 一页一页地存储
        origin_bid_info_data = []
        origin_text_data_list = []
        file_attach_list = []
        for i in range(len(url_list_href)):
            url_href = url_list_href[i]
            ori_href = ori_list_href[i]
            url = url_href.xpath("@href")[0]  # 公告链接
            bid_title = url_href.xpath("text()")[0].strip()  # 公告名称
            proj_id = get_uuid()  # 获取项目id.  #  此处还要存一个表。项目id，项目标题
            bid_id = get_uuid()
            proj_bid_list.append((proj_id, bid_id, create_time, operator))
            ori_info = ori_href.xpath('text()')
            release_time = ori_info[0].strip().split('|')[0].strip()  # 发布时间
            purchasing_agent = ori_info[0].strip().split('|')[1].strip().split('：')[1]  # 采购人
            agency = ori_info[0].strip().split('|')[2].strip().split('：')[1]  # 代理机构
            strong_info = ori_href.xpath('strong//text()')
            bid_type = strong_info[0].strip().split('|')[0]  # 标书类型
            project_type = strong_info[1].strip().split('|')[0]  # 项目类型
            region = ori_href.xpath('a//text()')  # 地区
            if len(region) != 0:
                region = region[0]
            origin_bid_data.append((0, bid_id, bid_title, bid_type, source, url, create_time, operator))
            bid_info_dict = {'release_time': release_time, 'purchasing_agent': purchasing_agent, 'agency': agency,
                             'bid_type': bid_type, 'project_type': project_type, 'region': region}

            origin_bid_info_data_list = _format_bid_info(bid_info_dict, bid_id, info_addr, create_time)
            origin_bid_info_data_table, origin_bid_text_data, files_attach = get_content(url, bid_id, proj_id)
            origin_bid_info_data.extend(origin_bid_info_data_list)
            origin_bid_info_data.extend(origin_bid_info_data_table)
            origin_text_data_list.append(origin_bid_text_data)
            file_attach_list.extend(files_attach)
        proj_bid_data = _format_r_projbid(proj_bid_list)
        rprojbid = RProjBid()  # r_proj_bid
        rprojbid.insertmany(proj_bid_data)
        origin_bid_info = OriginBidInfo()  # t_origin_bid_info
        origin_bid_info.insertmany(tuple(origin_bid_info_data))
        origin_bid_text = OriginBidText()  # t_origin_bid_text
        origin_bid_text.insertmany(tuple(origin_text_data_list))
        origin_bid = OriginBid()  # t_origin_bid
        print(len(origin_bid_data), '当前页面获取到的文章数')
        origin_bid.insertmany(tuple(origin_bid_data))  # 向 t_origin_bid添加数据
        file_attach_data = _format_file_attach(file_attach_list, create_time, operator)
        if len(file_attach_data) > 0:
            tfileattach = TFileAttach()  # t_file_attach
            tfileattach.insertmany(file_attach_data)

    while True:
        try:
            page = next(page_index)
            url = base_url.format(page, timeType)
            # print('当前列表页url:<{}>'.format(url))
            st = time.time()
            response = get_response(url, proxies, ipdata, msg)
            if response:
                deal_list_page(response)
                print(f'获取一页数据耗费时间: {time.time()-st}')
            else:
                print('获取列表页失败, proxies')
        except StopIteration:
            break


def get_content(url, bid_id, proj_id):  # 根据url获取正文
    ipdata = IpData()
    msg = ipdata.get_ipdata()
    proxies = ipdata.get_proxy(msg)
    create_time = datetime.datetime.now()
    create_time = trans_date_str(create_time)
    pattern = re.compile('(style.*/style)',re.I)
    def deal_response_content(response):

        def deal_table(selector):  # 获取概要
            info_addr = "ABSTRACT"
            table_list = selector.xpath('//div[@class="table"]/table/tr/td')
            if len(table_list) > 0:  # 获取到了指定元素
                title_list = selector.xpath('//div[@class="table"]/table/tr/td[contains(@class, "title")]')
                titles = []
                values = []
                for ele in table_list:
                    if ele in title_list:
                        titles.append(ele.xpath('text()')[0])
                    else:
                        if len(titles) > len(values):
                            value = ele.xpath('text()')
                            if value == []:
                                values.append('')
                            else:
                                values.append(value[0])
                        else:
                            pass
                href_list = selector.xpath('//div[@class="table"]/table/tr/td/a[contains(@title, "点击下载")]')
                file_url_list = []
                if len(href_list) > 0:
                    for href_ele in href_list:
                        url_suffix = href_ele.xpath('@id')[0]
                        file_url = "/oss/download?uuid={}".format(url_suffix)  # 目前前缀应该为 http://www.ccgp.gov.cn
                        file_url_list.append(file_url)
                    for i in range(1, len(file_url_list)+1):
                        values[-i] = file_url_list[-i]
                table = dict(zip(titles, values))
                biuld_bid_info_data = _format_bid_info(table, bid_id, info_addr, create_time)
                file_attach_ele = selector.xpath('//a[@class="bizDownload"]')  # 概要中的附件
                files = []
                if len(file_attach_ele) > 0:
                    for file in file_attach_ele:
                        file_name = file.xpath('text()')[0].strip()
                        file_url = file.xpath('@id')[0]
                        file_id = get_uuid()
                        files.append((file_name, file_url, file_id, bid_id, proj_id))
                return biuld_bid_info_data, files


        def deal_content(selector):  # 获取正文
            content_list = selector.xpath('//div[@class="vF_detail_content"]//text()')
            content_value = ''
            if len(content_list) > 0:  # 获取到了指定元素
                for content in content_list:
                    content = content.replace('***', '\r\n').replace('&nbsp;', ' ')
                    if content.strip().startswith('<'):
                        pass
                    else:
                        content_value += content
            file_attach_ele = selector.xpath("//a[contains(@ignore, '1')]")  # 正文中的附件
            files = []
            if len(file_attach_ele) > 0:
                for file in file_attach_ele:
                    file_name = file.xpath('text()')
                    if len(file_name) > 0:
                        file_name = file_name[0]
                        file_url = file.xpath('@href')[0]
                        if file_url == 'javascript:;':
                            continue
                        if file_url == '':
                            file_url = file.xpath('@id')[0]
                        file_id = get_uuid()
                        files.append((file_name, file_url, file_id, bid_id, proj_id))


            origin_bid_text_data = (0, bid_id, content_value, 1, 0, create_time, operator)
            return origin_bid_text_data, files

        response_text = response.text.encode(web_encoding).decode("utf-8")
        response_text = response_text.replace('</p>', '***</p>').replace('</h>', '***</h>').replace('<br>', '***<br>')
        style_value = pattern.findall(response_text)
        if len(style_value) > 0:
            for style in style_value:
                response_text = response_text.replace(style, '')
        baseSelector = etree.HTML(response_text, etree.HTMLParser())
        bid_info_data_table, file_table = deal_table(baseSelector)  # 获取概要
        bid_text_data, file_text = deal_content(baseSelector)  # 获取正文
        file_table.extend(file_text)
        return bid_info_data_table, bid_text_data, file_table
    # print('当前url为：', url)
    response = get_response(url, proxies, ipdata, msg)
    if response:
        return deal_response_content(response)



if __name__ == "__main__":
    num = 5  # 一页20只公告
    get_detail_url(base_url, num)




#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from mySpider.database.mongo import MongoProxy
from mySpider.spider.fetch import get_resp
from mySpider.spider.fetch import get_soup_without_throttle


__all__ = [
    'scan_proxies',
]


proxies_homes = {
    'cnproxy': 'http://cn-proxy.com/',
    'freeproxy': 'http://www.freeproxylists.net/zh/?c=CN&pr=HTTP', # 单页面
    'getproxy': 'http://www.getproxy.jp/cn/china',
    'goubanjia': 'http://www.goubanjia.com/free/gngn/index.shtml',
}


def scan_proxies():
    mongo_proxy = MongoProxy()
    
    proxies_list = []
    proxies_list += proxies_from_haoip()
    # proxies_list += proxies_from_xicidaili()
    proxies_list += proxies_from_kuaidaili()
    proxies_list += proxies_from_iphai()
    proxies_list += proxies_from_ip181()
    proxies_list += proxies_from_httpdaili()
    
    with open('proxies.txt', 'w') as f:
        f.write(str(proxies_list))
    
    print(len(proxies_list))
    for ip_port in iter(proxies_list):
        print('check {}@{}'.format(ip_port[0], ip_port[1]))
        if check_proxies(ip_port[0], ip_port[1]) \
                or check_valid(ip_port[0], ip_port[1]):
            mongo_proxy.push(ip_port[0], ip_port[1])
            print(ip_port[0], ip_port[1])
        

def proxies_from_haoip(url_home='http://haoip.cc/tiqu.htm'):
    proxies = []
    
    soup = get_soup_without_throttle(url_home)
    s = soup.select('.col-xs-12')[0].get_text()
    l = s.split('\n')
    for i, v in enumerate(l):
        l[i] = v.strip()
        if l[i]:
            vals = l[i].split(':')
            proxies.append([vals[0], vals[1]])

    return proxies

def proxies_from_xicidaili(url_home='http://www.xicidaili.com/wt/'):
    proxies = []
    urls = ['{}{}'.format(url_home, i) for i in range(1, 60)]
    
    for url in urls:
        time.sleep(1)
        soup = get_soup_without_throttle(url)
        
        trs = soup.table.tr.find_next_siblings()
        for tr in trs:
            td_ip = tr.td.find_next_sibling()
            ip = td_ip.get_text().strip()
            port = td_ip.find_next_sibling().get_text().strip()
            
            proxies.append([ip, port])
    
    return proxies

def proxies_from_kuaidaili(url_home='http://www.kuaidaili.com/proxylist/'):
    proxies = []
    urls = ['{}{}'.format(url_home, i) for i in range(1, 11)]
    
    for url in urls:
        time.sleep(1)
        soup = get_soup_without_throttle(url)
        
        trs = []
        trs.append(soup.table.tbody.tr)
        trs += trs[0].find_next_siblings()
        
        for tr in trs:
            td_ip = tr.td
            ip = td_ip.get_text().strip()
            port = td_ip.find_next_sibling().get_text().strip()
            
            proxies.append([ip, port])
    
    return proxies

def proxies_from_ip181(url_home='http://www.ip181.com/'):
    proxies = []
    
    soup = get_soup_without_throttle(url_home)
    
    trs = soup.table.tr.find_next_siblings()
    for tr in trs:
        ip_td = tr.td
        ip = ip_td.get_text().strip()
        port = ip_td.find_next_sibling().get_text().strip()

        proxies.append([ip, port])
    
    return proxies

def proxies_from_iphai(url_home='http://www.iphai.com/free/ng'):
    proxies = []
    
    soup = get_soup_without_throttle(url_home)
    trs = soup.table.tr.find_next_siblings()
    
    for tr in trs:
        td_ip = tr.td
        ip = td_ip.get_text().strip()
        port = td_ip.find_next_sibling().get_text().strip()

        proxies.append([ip, port])

    return proxies

def proxies_from_httpdaili(url_home='http://www.httpdaili.com/mfdl/'):
    proxies = []
    
    soup = get_soup_without_throttle(url_home)
    
    trs = soup.table.tr.find_next_siblings()
    for tr in trs:
        if tr.td:
            td_ip = tr.td
            ip = td_ip.get_text().strip()
            port = td_ip.find_next_sibling().get_text().strip()
            print(ip, port)

            proxies.append([ip, port])

    return proxies
    
# img 验证码识别
# http://proxy.mimvp.com/common/ygrandimg.php?id=1&port=MmTiIm4vMpDgw

def ip_port_to_proxy(ip, port):
    ip_port = '{}{}:{}'.format('http://', ip, port)
    proxy = {'http': ip_port}
    return proxy

def check_valid(ip, port):
    proxy = ip_port_to_proxy(ip, port)
    resp, status_code = get_resp('http://www.baidu.com', proxies=proxy)
    return status_code
    
def check_proxies(ip, port):
    check_url = 'http://ip.chinaz.com/getip.aspx'

    proxy = ip_port_to_proxy(ip, port)
    soup = get_soup_without_throttle(url=check_url, proxies=proxy)
    if soup:
        check_ip = soup.p.get_text().split("'")[1]
        return True if check_ip == ip else False
    else:
        return False

def main():
    print('Running {}...'.format(__file__))
    scan_proxies()

if __name__ == '__main__':
    main()

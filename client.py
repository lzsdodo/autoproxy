#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep

# Config
SLEEP_TIME = 2.5
AUTH = (user, passwd)
HOST = host


url_check_status = 'http://{}:5000/status/'.format(HOST)
url_receive_status = 'http://{}:5000/status/?act=receive'.format(HOST)
url_check_proxy = 'http://{}:5000/proxy/'.format(HOST)
url_set_proxy = 'http://{}:5000/proxy/?act=set'.format(HOST)


def get_req(url, auth=None):
    from requests import get
    return get(url, headers={'connection': 'close'}, stream=False, auth=auth)

def check_status():
    status = get_req(url_check_status).text
    return True if status == 'True' else False

def receive_status():
    result = get_req(url_receive_status).text
    return True if result == 'Done' else False

def set_new_proxy():
    old_proxy = get_req(url_check_proxy, auth=AUTH).text
    sleep(0.25)
    result = get_req(url_set_proxy, auth=AUTH).text
    sleep(0.25)
    new_proxy = get_req(url_check_proxy, auth=AUTH).text
    
    from datetime import datetime
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if result == 'Done' and proxy != new_proxy:
        print('[{}]: {} change to {}.'.format(now, proxy, new_proxy), file=open('proxy.log', 'a'))
        return True
    else:
        print('[{}]: error happened when changing proxy {} to {}.'.format(now, proxy, new_proxy), file=open('proxy.log', 'a'))
        return False

def reset_ip():
    from os import system as cmd
    cmd('pppoe-stop')
    sleep(0.2)
    cmd('pppoe-start')
    sleep(0.8)


if __name__ == '__main__':
    from os import path
    from os import chdir
    fpath, fname = path.split(path.abspath(__file__))
    chdir(fpath)
    
    while 1:
        sleep(SLEEP_TIME)
        if check_status():
            reset_ip()
            if(set_new_proxy()):
                receive_status()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    'Proxy',
]

AUTH = (user, passwd)
HOST = host


class Proxy(object):
    proxy = '0.0.0.0:6666'
    
    def __init__(self, host=HOST, auth=AUTH):
        self._host = host
        self._auth = auth
        
        self._url_check_status = 'http://{}:5000/status/'.format(host)
        self._url_change_status = 'http://{}:5000/status/?act=change'.format(host)
        self._url_check_proxy = 'http://{}:5000/proxy/'.format(host)
        
        self.proxy = self.init_proxy()
        

    def init_proxy(self):
        self.proxy = self.get_proxy()
        if self.proxy == '0.0.0.0:6666':
            self.set_new_proxy()
        Proxy.proxy = self.proxy
        return self.proxy

    @staticmethod
    def get_resp(url, auth=None):
        try:
            import requests
        except ImportError as e:
            raise('ImportError: {}'.format(e))
        
        try:
            text = requests.get(url, auth=auth, timeout=30).text
            return text
        except Exception as e:
            raise('Exception: {}'.format(e))

    def check_status(self):
        status = self.get_resp(self._url_check_status)
        return True if status == 'True' else False
    
    def change_proxy(self):
        status = self.get_resp(self._url_change_status)
        return True if status == 'Done' else False

    def get_proxy(self):
        return self.get_resp(self._url_check_proxy, auth=self._auth)
    
    def set_new_proxy(self):
        old_proxy = self.proxy
        if self.change_proxy():
            from time import sleep
            while self.check_status():
                sleep(3)
        new_proxy = self.get_proxy()
        
        if new_proxy == '0.0.0.0:6666':
            print('Server maybe restart.')
            self.set_new_proxy()
        else:
            self.proxy = new_proxy
            Proxy.proxy = new_proxy
        
        print('{} to {}'.format(old_proxy, new_proxy))

def test_Proxy():
    proxy = Proxy()
    print('Instance {} & Class {}'.format(proxy.proxy, Proxy.proxy))
    proxy.set_new_proxy()
    print('Instance {} & Class {}'.format(proxy.proxy, Proxy.proxy))

def main():
    print('Running {}...'.format(__file__))
    test_Proxy()

if __name__ == '__main__':
    main()

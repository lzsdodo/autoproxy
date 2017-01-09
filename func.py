#!/usr/bin/env python3
# -*- coding: utf-8 -*-

AUTH = (user, passwd)
HOST = host


class Proxy(object):
	_host = ''
	_auth = ''
	_url_check_status = ''
	_url_change_status = ''
	_url_check_proxy = ''

	proxy = ''
	
	def __init__(self):
		pass

	@classmethod
	def init(cls, host=HOST, auth=AUTH):
		cls._host = host
		cls._auth = auth
		cls._url_check_status = 'http://{}:5000/status/'.format(host)
		cls._url_change_status = 'http://{}:5000/status/?act=change'.format(host)
		cls._url_check_proxy = 'http://{}:5000/proxy/'.format(host)
		
		cls.proxy = '0.0.0.0:6666'
	
	@classmethod
	def get_req(cls, url, auth=None):
		try:
			from requests import get
		except ImportError as e:
			raise('ImportError: {}'.format(e))
		else:
			return get(url, headers={'connection': 'close'}, stream=False, auth=auth)
	
	@classmethod
	def check_status(cls):
		status = cls.get_req(cls._url_check_status).text
		return True if status == 'True' else False
	
	@classmethod
	def change_proxy(cls):
		status = cls.get_req(cls._url_change_status).text
		return True if status == 'Done' else False

	@classmethod
	def get_proxy(cls):
		return cls.get_req(cls._url_check_proxy, auth=cls._auth).text
	
	@classmethod
	def get_new_proxy(cls):
		old_proxy = cls.proxy
		
		if cls.change_proxy():
			from time import sleep
			while cls.check_status():
				sleep(3)
		
		cls.proxy = cls.get_proxy()
		return True if cls.proxy != old_proxy else None

	@classmethod
	def set_proxy(cls):
		cls.proxy = cls.get_proxy()


def test_Proxy():
	Proxy.init()
	Proxy.set_proxy()
	print(Proxy.proxy)
	Proxy.get_new_proxy()
	print(Proxy.proxy)

def main():
	print('Running {}...'.format(__file__))
	test_Proxy()

if __name__ == '__main__':
	main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

AUTH = (user, passwd)
HOST = host

url_check_status = 'http://{}:5000/status/'.format(HOST)
url_change_status = 'http://{}:5000/status/?act=change'.format(HOST)
url_check_proxy = 'http://{}:5000/proxy/'.format(HOST)

def get_req(url, auth=None):
	from requests import get
	return get(url, headers={'connection': 'close'}, stream=False, auth=auth)

def check_status():
	status = get_req(url_check_status).text
	return True if status == 'True' else False
	
def change_proxy():
	status = get_req(url_change_status).text
	return True if status == 'Done' else False

def get_proxy():
	return get_req(url_check_proxy, auth=AUTH).text

def get_new_proxy():
	proxy = get_proxy()
	
	if change_proxy():
		while check_status():
			from time import sleep
			sleep(2)
	
	new_proxy = get_proxy()
	return new_proxy if new_proxy != proxy else None	


def main():
	print('Running {}...'.format(__file__))
	new_proxy = get_new_proxy()
	print(new_proxy)

if __name__ == '__main__':
	main()

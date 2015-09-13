from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

def changed_byte(l1, l2, o):
	for i in range(o,len(l1)):
		if l1[i] != l2[i]:
			return i
	return -1

def replace_char(s, i, c):
	r = s
	if i == 0:
		r = c + s[i+1:]
	else:
		r = s[:i] + c + s[i+1:]
	return r
	


driver = webdriver.Firefox()
driver.get("http://bow.chal.mmactf.link/~scs/crypt6.cgi")
d = [[-1, -1]]*45

req = chr(1)*45
elem = driver.find_element_by_name("s")
elem.send_keys(req)
elem.send_keys(Keys.RETURN)
time.sleep(1)
elem = driver.find_element_by_name("s")
elem.send_keys('\b'*100)
m = re.search('/h1>(.+) <form', driver.page_source)
bytes = m.group(1).split()

for i in range(45):
	if i == 1:
		continue
	print '[*] Search for',i	
	power = -1
	addict = -1
	req2 = replace_char(req, i, chr(3))
	elem.send_keys(req2)
	elem.send_keys(Keys.RETURN)
	time.sleep(1)
	elem = driver.find_element_by_name("s")
	elem.send_keys('\b'*100)
	m = re.search('/h1>(.+) <form', driver.page_source)
	bytes2 = m.group(1).split()

	off = changed_byte(bytes, bytes2,0)
	t = int(bytes2[off],16) / int(bytes[off],16)
	if t == 4:
		power = off
	elif t == 3:
		addict = off
	else:
		print '[!] found unknown component'
		print '[!] multiplier is',t

	off = changed_byte(bytes, bytes2, off+1)
	t = int(bytes2[off],16) / int(bytes[off],16)
	if t == 4:
		if power != -1:
			print '[!] power component is alread found'
		else:
			power = off
	elif t == 3:
		if addict != -1:
			print '[!] addict component already found'
		else:
			addict = off
	else:
		print '[!] found unknown component'
		print '[!] multiplier is',t

	if addict > -1:
		d[addict] = list(d[addict])
		d[addict][0] = i
	if power > -1:	
		d[power] = list(d[power])
		d[power][1] = i
	print '[+] byte',i,'= byte',addict,'* 2**byte'+str(power)
print d
print 'Finished'


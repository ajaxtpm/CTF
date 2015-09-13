from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

driver = webdriver.Firefox()

driver.get("http://bow.chal.mmactf.link/~scs/crypt2.cgi")
s = '36 36 2a 64 4b 4b 4a 21 1e 4b 1f 20 1f 21 4d 4b 1b 1d 19 4f 21 4c 1d 4a 4e 1c 4c 1b 22 4f 22 22 1b 21 4c 20 1d 4f 1f 4c 4a 19 22 1a 66'
#driver.get("http://bow.chal.mmactf.link/~scs/crypt4.cgi")
#s = 'e3 e3 83 21 33 96 23 43 ef 9a 9a 05 18 c7 23 07 07 07 c7 9a 04 33 23 07 23 ef 12 c7 04 96 43 23 23 18 04 04 05 c7 fb 18 96 43 ef 43 ff'

d = dict()
for i in list('abcdef0123456789MA{}'):
	print "[*] Getting", i
	elem = driver.find_element_by_name("s")
	elem.send_keys(i)
	elem.send_keys(Keys.RETURN)
	elem = driver.find_element_by_name("s")
	elem.send_keys('\b')
	m = re.search('h1>(\w\w) <form', driver.page_source)
	d[int(m.group(1), 16)] = i
flag = ''
for i in s.split(): flag = flag + d[int(i,16)]
print '[+] Flag is',flag
print 'Finished'

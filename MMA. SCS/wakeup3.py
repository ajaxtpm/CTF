from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

driver = webdriver.Firefox()
driver.get("http://bow.chal.mmactf.link/~scs/crypt5.cgi")
d = dict()
s = '00 0c 3a 1e 52 02 53 02 51 0c 5d 56 51 5a 5f 5f 5a 51 00 05 53 56 0a 5e 00 52 05 03 51 50 55 03 04 52 04 0f 0f 54 52 57 03 52 04 4e'

alphabet='abcdefg0123456789}'

answer = 'MMA{'
hash1 = ''

while hash1 != s:
	for i in list(alphabet):
		elem = driver.find_element_by_name("s")
		elem.send_keys(answer+i)
		elem.send_keys(Keys.RETURN)
		time.sleep(1)
		elem = driver.find_element_by_name("s")
		elem.send_keys('\b'*100)
		m = re.search('h1>\w\w (.+) <form', driver.page_source)
		hash2 = m.group(1)
		if s.find(hash2) >= 0:
			answer = answer + i
			hash1 = hash2
			print '[+] found:', answer
			break
		
print answer
print 'Finished'


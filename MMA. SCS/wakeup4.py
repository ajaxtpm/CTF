from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

def replace_char(s, i, c):
	r = s
	if i == 0:
		r = c + s[i+1:]
	else:
		r = s[:i] + c + s[i+1:]
	return r

d = [[22, 21], [0, -1], [23, 22], [2, -1], [24, 23], [4, 3], [25, 24], [6, 5], [26, 25], [8, 7], [27, 26], [10, 9], [28, 27], [12, 11], [29, 28], [14, 13], [30, 29], [16, 15], [31, 30], [18, 17], [32, 31], [20, 19], [33, 32], [-1, 0], [34, 33], [5, 4], [35, 34], [9, 8], [36, 35], [13, 12], [37, 36], [17, 16], [38, 37], [21, 20], [39, 38], [7, 6], [40, 39], [15, 14], [41, 40], [3, 2], [42, 41], [19, 18], [43, 42], [11, 10], [44, 43]]
cipher = '62 a9 6c 28 0e 33 31 c6 68 cd 66 66 59 46 cc 53 0c 98 31 65 c6 35 c9 a9 60 4e 37 b0 33 46 0d 60 46 26 66 33 cc e6 a9 f6 6c 07 2b 23 af'.split()


driver = webdriver.Firefox()
driver.get("http://bow.chal.mmactf.link/~scs/crypt6.cgi")

answer = 'MMA{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}'
elem = driver.find_element_by_name("s")



def check_is_known(index, s):
	return s[index] != 'x'

def get_correct_values(unknown, s, index):
	global elem
	res = []
	for i in list("abcdef0123456789"):
		req = replace_char(s, unknown, i)
		elem.send_keys(req)
		elem.send_keys(Keys.RETURN)
		elem = driver.find_element_by_name("s")
		elem.send_keys('\b'*100)
		m = re.search('/h1>(.+) <form', driver.page_source)
		bytes = m.group(1).split()
		if bytes[index] == cipher[index]:
			res.append(i)
	return res

def get_unknown(pair, s):
	if not check_is_known(pair[0], s):
		return pair[0]
	if not check_is_known(pair[1], s):
		return pair[1]
	return -1

while answer.find('x') > -1:
	found = False	
	for k in range(len(d)):
		if check_is_known(d[k][0],answer) and check_is_known(d[k][1],answer):
			continue

		if (check_is_known(d[k][0],answer) and not check_is_known(d[k][1],answer)) \
		or (check_is_known(d[k][1],answer) and not check_is_known(d[k][0],answer)):
			unknown = get_unknown(d[k], answer)
			if unknown < 0:
				print '[!] Could not get unknown for',d[i],' Skipping'
				continue
			possible_values = get_correct_values(unknown, answer, k)
			if len(possible_values) > 1:
				print '[!] Ambiguous answers for',unknown,':',possible_values
			elif possible_values == []:
				print '[!] Could not find possible value for',unknown
				continue
			value = possible_values[0]
			found = True
			answer = answer[:unknown]+value+answer[unknown+1:]
			print '[*] Answer is',answer
			break
	if not found:
		print '[!] Cant find any else'
		break

print 'Finished'

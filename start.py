
#encoding:utf-8

import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  
import urllib.request
import codecs
import re
import time
import subprocess

url = "https://www.okcoin.cn/"

reg = r'<dt id="ltcLastPriceColor" class="green">¥<em id="ltcLastPrice">(.+)</em></dt>'
com = re.compile(reg)

#value of excepation
voe = 155
data = ''
counts = 0


def get_message(info):
	current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	message = '当前时间:' + current_time + '\n'
	message = message + '期望值：' + voe.strip() + '\n'
	message = message + '当前值：' + info.strip() + '\n'
	return message


def send_email(info):
	sender= '******'  
	receiver = '******'  
	subject = 'dobe,你有新消息'  
	smtpserver = 'smtp.sina.com'  
	username = sender  
	password = '****' 

	msg = MIMEText(info, 'plain', 'utf-8')#中文需参数‘utf-8’，单字节字符不需要  
	msg['Subject'] = Header(subject, 'utf-8')
	msg['From'] = sender
	msg['To'] = receiver  

	smtp = smtplib.SMTP()  
	smtp.connect(smtpserver)  
	smtp.login(username, password)  
	smtp.sendmail(sender, receiver, msg.as_string())  
	smtp.quit()  

def load_voe():
	global voe
	vff = open('./voe.flush')
	line = vff.readline()
	vff.close()
	if line.rstrip() == '1':
		vcf = open("voe.conf")
		voe = vcf.readline()
		vcf.close()
	return voe


def save_log(info):
	logf = codecs.open('./m.log','a','utf-8')
	logf.write(info)
	logf.write('\n')
	logf.close()


while 'true' :
	data = urllib.request.urlopen(url).read();
	data = data.decode("utf-8")

	#save to file
	#f = codecs.open('./tmp.txt','w','utf-8')
	#f.write(data)
	#f.close()
	#<dt id="ltcLastPriceColor" class="green">¥<em id="ltcLastPrice">165.97</em></dt>
	val = re.findall(com, data)
	ltb = val[0]


	if float(ltb) > float(load_voe()) :
		message = get_message(ltb)
		print(message)
		save_log(message)
		"""if counts < 1 :
			send_email(message)	
		counts += 1"""
	time.sleep(10)



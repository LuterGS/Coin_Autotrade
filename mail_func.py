import userdata
import smtplib
import file_writer as fileio

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

getter = userdata.getter()
sender = userdata.sender()
log_location = userdata.log_loc()

def reaching_point(percent, string):
	percent = str(percent)

	msg = MIMEMultipart()
	msg['Subject'] = 'Earn ' + percent + '% complete, set krw_money as 103%'
	msg['From'] = sender
	msg['To'] = getter
	msg.preamble = 'TEST'
	
	fp = open(log_location + 'main_log.txt', 'rb')
	_text = MIMEText(fp.read())
	fp.close()
	_text.add_header('Content-Disposition', 'attachment', filename='main_log.txt')
	msg.attach(_text)
	
	fp_2 = open(log_location + 'calculate_log.txt', 'rb')
	_text_2 = MIMEText(fp_2.read())
	fp_2.close()
	_text_2.add_header('Content-Disposition', 'attachment', filename='calcuate_log.txt')
	msg.attach(_text_2)
	
	fp_3 = open(log_location + 'nohup.out', 'rb')
	_text_3 = MIMEText(fp_3.read())
	fp_3.close()
	_text_3.add_header('Content-Disposition', 'attachment', filename='nohup_out.txt')
	msg.attach(_text_3)

	fp_4 = open(log_location + 'nohup.err', 'rb')
	_text_4 = MIMEText(fp_4.read())
	fp_4.close()
	_text_4.add_header('Content-Disposition', 'attachment', filename='nohup_err.txt')
	msg.attach(_text_4)


	composed = msg.as_string()
	smtpsv = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender, 'Lu-$W7#1:Na')
	smtpsv.sendmail(sender, getter, composed)
	smtpsv.quit()

	fileio.renew_log()

def danger_fall():
	text = 'Value is at Dangerous State, Need Attention'

	msg = MIMEText(text)
	msg['Subject'] = '30% Downfall detected, System break.'
	msg['From'] = sender
	msg['To'] = getter
	
	smtpsv = smtplib.SMTP('127.0.0.1', 1025)
	smtpsv.sendmail(sender, getter, msg.as_string())
	smtpsv.quit()



if __name__ == "__main__":
	reaching_point(10, 'Earn one time complete')

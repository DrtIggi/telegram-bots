import os
with open('/root/GOGO/except.txt','rb') as f:
	for x in f:
		if x!=b"\n":
			os.system("echo '' > /root/GOGO/except.txt")
			os.system('/usr/bin/python3 /root/GOGO/bot.py')
		else:
			pass


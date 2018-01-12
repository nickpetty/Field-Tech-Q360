import requests
import json
import urllib
import urllib2




class Q360(object):
	
	"""docstring for Q360"""
	def __init__(self, username, password):
		#super(Q360, self).__init__()
		self.url = "https://360.southcentralav.com/ajax/?_a=authenticate&_r=action=login"
		self.username = username
		self.password = password

	def login(self):

		
		headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
					"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
		payload = {'userid':'npetty', 'password':'Scav01234', 'touch':'false', 'shared':''}

		#response = requests.request("POST", self.url, data=payload)
		#r = requests.post(self.url, data=payload, headers=headers)

		data = urllib.urlencode(payload)
		req = urllib2.Request(self.url, data)
		resp = urllib2.urlopen(req)



		return resp.read()

		
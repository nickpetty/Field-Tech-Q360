import requests
import json

class Q360(object):
	"""docstring for Q360"""
	def __init__(self, username, password):
		#super(Q360, self).__init__()
		self.username = username
		self.password = password
		self.session = requests.Session()
		self.session.get("https://360.southcentralav.com/controller.php?action=q360")
		

	def login(self):
		url = "https://360.southcentralav.com/ajax/?_a=authenticate&_r=action%3Dlogin"
		data = {"userid":self.username, "password":self.password, "touch":"false", "shared":""}
		r = self.session.post(url, data=data)

		if json.loads(r.text)["success"] == True:
			return True
		else:
			return "LOGIN ERROR: " + str(json.loads(r.text))

	def tasks(self, username, enddate): #ENDDATE - i.e., 2018-12-24
		url = "https://360.southcentralav.com/ajax/" #?enddate=2018-01-11&numdays=0&userid=NPETTY&incltasksresp=Y&incltasksassign=Y&inclopptasks=Y&incloppor=Y&inclactivity=Y&inclquotes=Y&inclcalls=Y&inclcallscsr=Y&_limit=10000&_grid=mytasklist&_a=mytasklist&_r=action%3Dmytasklist%26window%3Ds0%26dhxr1513472264476%3D1"
		data = {"enddate":enddate, "userid":username, "_limit":10000, "numdays:":0, "incltasksresp":"Y", 
				"incltasksassign":"Y", "inclopptasks":"Y", "incloppor":"Y", "inclactivity":"Y", "inclquotes":"Y", 
				"inclcalls":"Y", "inclcallscsr":"Y", "_a":"mytasklist"}
				
		r = self.session.get(url, params=data)
		#return str(json.loads(r.text)["data"][0]['projecttitle'])
		respData = json.loads(r.text)['data'][0]
		taskData = {"projectTitle": str(respData['projecttitle']),
					"company":str(respData["company"]),
					"companyAddress":str(respData['siteaddress'])+" "+str(respData['sitecitystatezip']),
					"description":str(respData['description']),
					"comments":str(respData['resq_cell_note_comment']),
					"siteContact":str(respData['sitecontact']),
					"sitePhone":str(respData['sitephone']),
					"taskID":str(respData['itemno']),
					"date":str(respData['date'])}

		return str(taskData)
		#return str(json.loads(r.text)['data'][0])






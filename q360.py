import requests
import json
from lxml import html


class Q360(object):
	"""docstring for Q360"""
	def __init__(self):
		#super(Q360, self).__init__()
		self.url = "https://360.southcentralav.com/ajax/"

		self.users = {'session':requests.Session(), 'allTasks':{}}
		print '\rinit Q360 ----------------------------------------------\r'

	def login(self, username, password):
		url = "https://360.southcentralav.com/ajax/?_a=authenticate&_r=action%3Dlogin"
		data = {"userid":username, "password":password, "touch":"false", "shared":""}

		if username in self.users: # if user is logged in from same device or different
			r = self.users[username]['session'].post(url, data=data)

			if json.loads(r.text)["success"] == True:
				return True
			else:
				return False

		else: # if user is not logged in from any device
			session = requests.Session()
			session.get("https://360.southcentralav.com/controller.php?action=q360")
			
			r = session.post(url, data=data)

			if json.loads(r.text)["success"] == True:
				self.users[username] = {'session':session}
				return True
			else:
				return False

	def logout(self, username):
		self.users.pop(username, None)
		return True

	def tasks(self, username, sessionUser, enddate): #ENDDATE - format YYY-MM-DD

		### sessionUser to allow search of username different from the logged in user ###
		params = {"enddate":enddate, "userid":username, "_limit":10000, "numdays:":0, "incltasksresp":"Y", 
				"incltasksassign":"Y", "inclopptasks":"Y", "incloppor":"Y", "inclactivity":"Y", "inclquotes":"Y", 
				"inclcalls":"Y", "inclcallscsr":"Y", "_a":"mytasklist"}
				
		r = self.users[sessionUser]['session'].get(self.url, params=params)
		
		respData = json.loads(r.text)['data']
		allData = {"calls":{}, "tasks":{}}
		for item in respData:
			itemData = {"projectTitle": str(item['projecttitle']),
						"company":str(item["company"]),
						"companyAddress":str(item['siteaddress'])+" "+str(item['sitecitystatezip']),
						"description":str(item['description']),
						"comments":str(item['resq_cell_note_comment']),
						"siteContact":str(item['sitecontact']),
						"sitePhone":str(item['sitephone']),
						"taskID":str(item['itemno']),
						"date":str(item['date'])}

			if item['type'] == "Call":
				allData['calls'][str(item['itemno'])] = itemData

			if item['type'] == "SUBTASK": 
				allData['tasks'][str(item['itemno'])] = itemData

			
				page = self.users[sessionUser]['session'].get("https://360.southcentralav.com/controller.php?action=project_task_detail&id=" + str(item['itemno']))
				tree = html.fromstring(page.text)
				parentTaskID = tree.xpath('/html/body/div/div/form/div/div/div/div/div/p/label/a/@href')
				
				# Get parent ID....		
				allData['tasks'][str(item['itemno'])]['parentTaskID'] = parentTaskID[0][46:]
				
				allData['tasks'][str(item['itemno'])]['timebills'] = self.timebills(username, str(item['itemno']))
				allData['tasks'][str(item['itemno'])]['documents'] = self.documents(username, str(item['itemno']), parentTaskID[0][46:])


			if username == sessionUser: ### sessionUser to allow search of username different from the logged in user ###
				self.users[username]['allData'] = allData

		return allData
		

	def serviceCalls(self):
		pass

	def timebills(self, username, taskID):
	
		params = {"projectscheduleno":taskID, "_limit":10000, "_a":"timebillbyprojecttask"}
		r = self.users[username]['session'].get(self.url, params=params)

		return json.loads(r.text)['data']


	def documents(self, username, taskID, parentTaskID):
		
		params = {
				"linkno":taskID, 
				"linktype":"projtask", 
				"includesubtasks":"Y", 
				"_a":"documents_by_projectsubtask", 
				"parentprojectscheduleno":parentTaskID,
				"displayevents":"N",
				"_grid":"documents"
				}

		r = self.users[username]['session'].get(self.url, params=params)
		docs = json.loads(r.text)['data']

		return docs

	def download(self, username, docno):
		r = self.users[username]['session'].get('https://360.southcentralav.com/download/downloader.php?documentno=' + docno)

		return r.content





































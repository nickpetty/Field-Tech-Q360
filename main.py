from flask import Flask, render_template, jsonify, request, session, render_template_string, make_response, url_for, redirect, g
from q360 import Q360

import json

app = Flask(__name__)
app.secret_key = "babluebee"


q360 = Q360()


@app.route('/')
def index():
	#return render_template('index2.html')
	if session.get('loggedin') == True:
		return render_template('index2.html')
	else:
		return redirect('/login')


@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'GET':
		if session.get('loggedin') == None:
			return render_template('login.html', wrongAlert="")
		if session.get('loggedin') == True:
			return redirect('/')

	if request.method == 'POST':
		resp = q360.login(request.form['user'], request.form['password'])
		
		if resp == True:
			session['loggedin'] = True
			session['username'] = request.form['user']
			return redirect('/')
		else: # Wrong username or password
			session['loggedin'] = None
			wrongAlert = """
						<div id="wrongAlert" class="alert alert-danger" role="alert" style="width:80%;">
  							<strong>Wrong username or password</strong>
						</div>
						"""
			return render_template('login.html', wrongAlert=wrongAlert)

@app.route('/logout')
def logout():
	if q360.logout(session['username']) == True:
		session['loggedin'] = None
		return redirect('/')
	else:
		return "I didn't log out...."

@app.route('/tasks')
def tasks():
	if session.get('loggedin') == True:
		allData = q360.tasks(session.get('username'), session.get('username'), request.args.get('date'))
		renderedPanels = "<div id='tasksDiv' style='display:none;'>\n"

		for task in allData['tasks']: # Render Task's div
			renderedPanels += render_template('taskPanel.html', task=allData['tasks'][task]) + "\n"
		renderedPanels += "</div>\n<div id='callsDiv' style='display:none;'>"

		for call in allData['calls']:
			renderedPanels += render_template('callsPanel.html', call=allData['calls'][call]) + "\n"
		renderedPanels += "</div>\n"


		return render_template_string(renderedPanels)
	else:
		return redirect('/login')


@app.route('/download')
def downloadDoc():
	if session.get('loggedin') == True:
		pdf = q360.download(session.get('username'), request.args.get('docno'))
		response = make_response(pdf)
		response.headers['Content-Type'] = 'application/pdf'
		response.headers['Content-Disposition'] = \
		'inline; filename=%s' % request.args.get('docname')
		return response
	else:
		return redirect('/login')


@app.route('/debug')
def debug():
	allTasks = q360.tasks(session.get('username'), session.get('username'), request.args.get('date'))
	print str(allTasks)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)




















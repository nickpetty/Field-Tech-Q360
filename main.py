from flask import Flask, render_template, jsonify, request
from q360 import Q360

app = Flask(__name__)


@app.route('/')
def index():
	user = Q360('npetty', 'Scav01234')
	user.login()
	return user.tasks('NPETTY', '2018-01-11')
	

@app.route('/sign')
def sign():
	return render_template('test.html')





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
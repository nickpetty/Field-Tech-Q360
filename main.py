from flask import Flask, render_template, jsonify, request
from q360 import Q360

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	user = Q360('test', 'password')
	return user.login()
	

## Q360 API Requests ##

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
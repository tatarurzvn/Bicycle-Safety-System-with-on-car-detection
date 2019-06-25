from app import app
from flask import render_template
from time import sleep

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/_stream')
def stream_log():
    def generate():
    	try:
        	with open('/home/pi/Desktop/logs.log') as f:
        	    while True:
        	        yield f.read()
        	        sleep(3)
       	except Exception as err:
       		yield "File not found error"
    return app.response_class(generate(), mimetype='text/plain')


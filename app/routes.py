from app import app
from flask import render_template, jsonify
from time import sleep, asctime
from psutil import virtual_memory, cpu_percent
from datetime import datetime

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

@app.route('/_hardware_usage')
def hardware_usage():
    return jsonify(mem_use=str(virtual_memory()[2]) + r'%',
                   cpu_use=str(cpu_percent()) + r'%')

usage_history = list([["Time", "Memory", "Cpu"]])
@app.route('/_hardware_usage_gcharts')
def hardware_usage_gcharts():
    global usage_history
    max_data = 20

    if len(usage_history) > max_data:
        usage_history = usage_history[:1] + usage_history[2:]
    current_time = datetime.now()
    current_time = str(current_time.hour) + ":" + str(current_time.minute)
    new_data = [current_time, virtual_memory()[2], cpu_percent()]
    usage_history.append(new_data)
    return jsonify(usage_history)

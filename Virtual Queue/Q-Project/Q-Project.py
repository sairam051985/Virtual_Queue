from flask import Flask,url_for,render_template,Response,request,redirect,url_for
from flask_socketio import SocketIO,emit
import collections


#logging.basicConfig(filename=r'C:\Users\bhoos003\SAI\sai-lab\rtgdb-dashboard\venv\Logs\rtgdb_python.log', level=logging.INFO, format='%(asctime)s %(message)s')
app = Flask(__name__, static_url_path='/Static')
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio=SocketIO(app)
virtual_queue=collections.deque() 

@app.route('/')
def index():
	return app.send_static_file('index.html')
	
@app.route('/JoinQ')
def joinq():
	return app.send_static_file('joinq.html')
	
@app.route('/Newjoin', methods=['POST'])
def Newjoin():
	formvalues=request.form['customer']+'+'+request.form['email']+'+'+request.form['phone']
	try:
		if virtual_queue.index(formvalues):
			msg="Customer already waiting in queue at "+ str(virtual_queue.index(formvalues))
	except ValueError:
		virtual_queue.append(formvalues)
	
	return redirect(url_for('display'))
	
@app.route('/display')
def display():
	return render_template('Queue_Display.html',virtual_queue=virtual_queue)
	
@app.route('/remove', methods=['POST'])
def remove():
	data = request.get_json()
	print (data)
	x = int(data['row']['remove'])
	del virtual_queue[int(x)]
	print (virtual_queue)
	return redirect(url_for('display'))



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001,debug=True)
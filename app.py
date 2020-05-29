from threading import Lock
from datetime import date
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect  
import random
import MySQLdb 
import math
import time
import serial
import threading
import os
import MySQLdb
import ConfigParser

async_mode = None

app = Flask(__name__)

config = ConfigParser.ConfigParser()
config.read('config.cfg')
myhost = config.get('mysqlDB', 'host')
myuser = config.get('mysqlDB', 'user')
mypasswd = config.get('mysqlDB', 'passwd')
mydb = config.get('mysqlDB', 'db')

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

current_time=0
today=0

def background_thread(args):    
    argument = 0
    count = 1    
    dataList = []    
    while True:

            ser=serial.Serial('/dev/ttyS1', 9600)
            ser.baudrate=9600        
            read_ser=ser.read(2)
            print(read_ser)            
            try:
                read_ser2=float(read_ser)*(2*math.pi/60)        
                step=(float(read_ser)*100)/60
                freq=float(read_ser)/60
            except:
                read_ser=0
                read_ser2=0
                step=0
                freq=0
#             count += 1
         
              
                print(args)
                
    
        
                socketio.emit('my_response',
                          {'data': float(read_ser), 'datahours': float(round((read_ser2),2)),'datastep': float(round((step),2)),'datafreq': float(round((freq),2)),'count': count},
                          namespace='/test')
                count += 1
    #             print(read_ser)
        db.close
        socketio.sleep(2) 


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)
       
@app.route('/graphlive', methods=['GET', 'POST'])
def graphlive():
    return render_template('graphlive.html', async_mode=socketio.async_mode)

@app.route('/gauge', methods=['GET', 'POST'])
def gauge():
    return render_template('gauge.html', async_mode=socketio.async_mode)

@app.route('/tabsrs')
def tabs():
    return render_template('tabsrs.html', async_mode=socketio.async_mode)

@app.route('/tabsav')
def tabs1():
    return render_template('tabsav.html', async_mode=socketio.async_mode)

@app.route('/tabsms')
def tabs2():
    return render_template('tabsms.html', async_mode=socketio.async_mode)

@app.route('/tabsfr')
def tabs3():
    return render_template('tabsfr.html', async_mode=socketio.async_mode)


@socketio.on('my_event', namespace='/test')
def test_message(message5):
    today=date.today()
    d1=today.strftime("%d/%m/%Y")
    session['date'] = d1

@socketio.on('db_event', namespace='/test')
def db_message(message):   
    session['db_value'] = message['value']  


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    print("\nDISCONNECTED\nPOIT 2020 by Roman Kmotorka ")
    os._exit(0)
    

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())            


@socketio.on('click_event', namespace='/test')
def db2_message(message2):
    global connected
    if connected:        
        connected = 0
        print("\nMONITORING ENDED")
    else:
        connected = 1
        print("\nMONITORING STARTED")

        
@socketio.on('start_event', namespace='/test')
def db3_message(message3):
    global begin
    if begin:        
        begin = 1        
    else:
        begin = 1
        print("\nCONNECTED")

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)
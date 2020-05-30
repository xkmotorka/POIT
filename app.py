from threading import Lock
from datetime import date
import datetime
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
connected = 0
begin=0
current_time=0
today=0
datab=5
a='#'
b='\n'
i=1
x=0

def background_thread(args):    
    count = 1    
    dataList = []
    db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
    
    maxRS=0
    minRS=100
    criticalRS=0
    
    sumRS=0
    maxAV=0
    minAV=10.47
    criticalAV=0
    sumAV=0
    maxMS=0
    minMS=166.67
    criticalMS=0
    sumMS=0
    maxFR=0
    minFR=1.67
    criticalFR=0
    sumFR=0    
    fo = open("static/files/Rotational_speed.txt","a+")
    fo2 = open("static/files/Angular_velocity.txt","a+")
    fo3 = open("static/files/Motor_speed.txt","a+")
    fo4 = open("static/files/Frequency.txt","a+")
    fo1515 = open("static/files/ALL.txt","a+")
    file1='/home/pi/POIT_zadanie/static/files/Rotational_speed.txt'
    file2='/home/pi/POIT_zadanie/static/files/Angular_velocity.txt'
    file3='/home/pi/POIT_zadanie/static/files/Motor_speed.txt'
    file4='/home/pi/POIT_zadanie/static/files/Frequency.txt'
    file1515='/home/pi/POIT_zadanie/static/files/ALL.txt'
    str2 = "\r"
    str22 = "\r"
    str222 = "\r"
    str2222 = "\r"
    str1515 = "\r\n"
    if os.stat(file1).st_size==0:
        nadpis="Max Rotational Speed = 99 RPM\nCritical value = 80 RPM\nUnits: RPM" 
        str1 = str(nadpis)
        str3 = str1 + str2    
        fo.write(str3)
        fo.close    
    if os.stat(file2).st_size==0:
        nadpis2="Max Angular Velocity = 10.37 rad/s\nCritical value = 8.38 rad/s\nUnits: rad/s" 
        str11 = str(nadpis2)
        str33 = str11 + str22    
        fo2.write(str33)
        fo2.close    
    if os.stat(file3).st_size==0:
        nadpis3="Max Motor Speed = 165 steps/s\nCritical value = 133.33 steps/s\nUnits: steps/s" 
        str111 = str(nadpis3)
        str333 = str111 + str222    
        fo3.write(str333)
        fo3.close    
    if os.stat(file4).st_size==0:
        nadpis4="Max Frequency = 1.59 HZ\nCritical value = 1.33 Hz\nUnits: Hz" 
        str1111 = str(nadpis4)
        str3333 = str1111 + str2222    
        fo4.write(str3333)
        fo4.close
        
    while True:
        if begin:
            ser=serial.Serial('/dev/ttyS1', 9600)
            ser.baudrate=9600        
            read_ser=ser.read(2)
            if connected:
                global i
                if i>0:
                    print "#1"
                    i=0
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
            if args:          
              dbV = dict(args).get('db_value')
            else:          
              dbV = 'nieco'
              
            if count == 21 or count == 41 or count == 61 or count == 81 or count == 101 or count == 121 or count == 141 or count == 161 or count == 181 or count == 201 or count == 221 or count == 241 or count == 261 or count == 281 or count == 301:
                dataDict600 = {
                "Max achieved rotational speed from the last 20 samples": int(maxRS)                     
                }
                dataDict601 = {
                "Min achieved rotational speed from the last 20 samples": int(minRS)                                   
                }
                dataDict602 = {
                "Average rotational speed from the last 20 samples": float(round((sumRS/20),2))           
                }
                dataDict603 = {
                "Number of critical values from the last 20 samples": int(criticalRS)                        
                }
             
                prem600 = str(dataDict600).replace("'", "\"")       
                str600 = str(prem600)
                str3600 = str600 + str2
                
                prem601 = str(dataDict601).replace("'", "\"")       
                str601 = str(prem601)
                str3601 = str601 + str2
                
                prem602 = str(dataDict602).replace("'", "\"")       
                str602 = str(prem602)
                str3602 = str602 + str2
                
                prem603 = str(dataDict603).replace("'", "\"")       
                str603 = str(prem603)
                str3603 = str603 + str2
                
                fo = open("static/files/Rotational_speed.txt","a+")
                fo.write(str3600)
                fo.write(str3601)
                fo.write(str3602)
                fo.write(str3603)
                fo.close
                
                dataDict700 = {
                "Max achieved angular velocity from the last 20 samples": float(round((maxAV),2))                      
                }
                dataDict701 = {
                "Min achieved angular velocity from the last 20 samples": float(round((minAV),2))                                    
                }
                dataDict702 = {
                "Average angular velocity from the last 20 samples": float(round((sumAV/20),2))        
                }
                dataDict703 = {
                "Number of critical values from the last 20 samples": int(criticalAV)   
                } 
             
                prem700 = str(dataDict700).replace("'", "\"")       
                str700 = str(prem700)
                str3700 = str700 + str2
                
                prem701 = str(dataDict701).replace("'", "\"")       
                str701 = str(prem701)
                str3701 = str701 + str2
                
                prem702 = str(dataDict702).replace("'", "\"")       
                str702 = str(prem702)
                str3702 = str702 + str2
                
                prem703 = str(dataDict703).replace("'", "\"")       
                str703 = str(prem703)
                str3703 = str703 + str2
                
                fo2 = open("static/files/Angular_velocity.txt","a+")
                fo2.write(str3700)
                fo2.write(str3701)
                fo2.write(str3702)
                fo2.write(str3703)
                fo2.close
                
                dataDict800 = {
                "Max achieved motor speed from the last 20 samples": float(round((maxMS),2))                      
                }
                dataDict801 = {
                "Min achieved motor speed from the last 20 samples": float(round((minMS),2))                                    
                }
                dataDict802 = {
                "Average motor speed from the last 20 samples": float(round((sumMS/20),2))   
                }
                dataDict803 = {
                "Number of critical values from the last 20 samples": int(criticalMS)                                        
                } 
             
                prem800 = str(dataDict800).replace("'", "\"")       
                str800 = str(prem800)
                str3800 = str800 + str2
                
                prem801 = str(dataDict801).replace("'", "\"")       
                str801 = str(prem801)
                str3801 = str801 + str2
                
                prem802 = str(dataDict802).replace("'", "\"")       
                str802 = str(prem802)
                str3802 = str802 + str2
                
                prem803 = str(dataDict803).replace("'", "\"")       
                str803 = str(prem803)
                str3803 = str803 + str2
                
                fo3 = open("static/files/Motor_speed.txt","a+")
                fo3.write(str3800)
                fo3.write(str3801)
                fo3.write(str3802)
                fo3.write(str3803)
                fo3.close
                
                dataDict900 = {
                "Max achieved frequency from the last 20 samples": float(round((maxFR),2))                   
                }
                dataDict901 = {
                "Min achieved frequency from the last 20 samples": float(round((minFR),2))                                     
                }
                dataDict902 = {
                "Average frequency from the last 20 samples": float(round((sumFR/20),2))      
                }
                dataDict903 = {
                "Number of critical values from the last 20 samples": int(criticalFR)                        
                }
             
                prem900 = str(dataDict900).replace("'", "\"")       
                str900 = str(prem900)
                str3900 = str900 + str2
                
                prem901 = str(dataDict901).replace("'", "\"")       
                str901 = str(prem901)
                str3901 = str901 + str2
                
                prem902 = str(dataDict902).replace("'", "\"")       
                str902 = str(prem902)
                str3902 = str902 + str2
                
                prem903 = str(dataDict903).replace("'", "\"")       
                str903 = str(prem903)
                str3903 = str903 + str2
                
                fo4 = open("static/files/Frequency.txt","a+")
                fo4.write(str3900)
                fo4.write(str3901)
                fo4.write(str3902)
                fo4.write(str3903)
                fo4.close 
     
                maxRS=0
                minRS=100
                criticalRS=0
                sumRS=0
                maxAV=0
                minAV=10.47
                criticalAV=0
                sumAV=0
                maxMS=0
                minMS=166.67
                criticalMS=0
                sumMS=0
                maxFR=0
                minFR=1.67
                criticalFR=0
                sumFR=0
                
            if connected:
                if args:          
                    dbV = args.get('db_value')
                else:          
                    dbV = 'nieco'  
                if float(read_ser) > float(maxRS):
                    maxRS = read_ser
                if float(read_ser) < float(minRS):
                    minRS = read_ser
                if float(read_ser) >= 80:            
                    criticalRS+=1
                    
                if float(read_ser2) > float(maxAV):
                    maxAV = read_ser2
                if float(read_ser2) < float(minAV):
                    minAV = read_ser2
                if float(read_ser2) >= 8.38:
                    criticalAV+=1
                    
                if float(step) > float(maxMS):
                    maxMS = step
                if float(step) < float(minMS):
                    minMS = step
                if float(step) >= 133.33:
                    criticalMS+=1
                
                if float(freq) > float(maxFR):
                    maxFR = freq
                if float(freq) < float(minFR):
                    minFR = freq
                if float(freq) >= 1.33:
                    criticalFR+=1
                sumRS+=int(read_ser)
                sumAV+=float(read_ser2)
                sumMS+=float(step)
                sumFR+=float(freq)           
              
#                 print(args)
                
                if datab == 0:
                  dataDict1515 = {
                    "No": count, 
                    "RS": int(read_ser),
                    "AV": round(float(read_ser2),2),
                    "MS": round(float(step),2),
                    "FR": round(float(freq),2)
                    }
                  dataList.append(dataDict1515)
                else:
                  if len(dataList)>0:                
                    prem1515 = str(dataList).replace("'", "\"")
                    print prem1515                
                    str1516 = str(prem1515)
                    str1517 = str1516 + str1515
                    fo1515 = open("static/files/ALL.txt","a+")
                    fo1515.write(str1517)
                    fo1515.close
                    cursor = db.cursor()
                    cursor.execute("SELECT MAX(id) FROM graph")
                    maxid = cursor.fetchone()
                    cursor.execute("INSERT INTO graph (id, hodnoty) VALUES (%s, %s)", (maxid[0] + 1, prem1515))
                    db.commit()
                  dataList = []            
            
                dataDict = {
                    "Rotational Speed": int(read_ser),
                    "Sample No.": count              
                }     
                prem = str(dataDict).replace("'", "\"")       
                str1 = str(prem)
                str3 = str1 + str2
                fo = open("static/files/Rotational_speed.txt","a+")
                fo.write(str3)
                fo.close
                
                dataDict2 = {
                    "Angular Velocity": round(float(read_ser2),2),
                    "Sample No.": count              
                }        
                prem2 = str(dataDict2).replace("'", "\"")
                str11 = str(prem2)
                str33 = str11 + str22
                fo2 = open("static/files/Angular_velocity.txt","a+")
                fo2.write(str33)
                fo2.close
                
                dataDict3 = {
                    "Sample No.": count,
                    "Motor Speed": round(float(step),2)                        
                }          
                prem3 = str(dataDict3).replace("'", "\"")
                str111 = str(prem3)
                str333 = str111 + str222
                fo3 = open("static/files/Motor_speed.txt","a+")
                fo3.write(str333)
                fo3.close
                
                dataDict4 = {
                    "Frequency": round(float(freq),2),
                    "Sample No.": count            
                }               
                prem4 = str(dataDict4).replace("'", "\"")
                str1111 = str(prem4)
                str3333 = str1111 + str2222
                fo4 = open("static/files/Frequency.txt","a+")
                fo4.write(str3333)
                fo4.close           
        
                socketio.emit('my_response',
                          {'data': float(read_ser), 'datahours': float(round((read_ser2),2)),'datastep': float(round((step),2)),'datafreq': float(round((freq),2)),'count': count},
                          namespace='/test')
                count += 1
                print('%s%s%d'%(b,a,count))  
    #             print(read_ser)
        db.close
        socketio.sleep(2) 

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)       

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

@app.route('/tabs')
def tabs4():
    return render_template('tabs.html', async_mode=socketio.async_mode)

@app.route('/db')
def db():
  db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
  cursor = db.cursor()
  cursor.execute('''SELECT  hodnoty FROM  graph''')
  rv = cursor.fetchall()
  return str(rv)    

@app.route('/dbdata/<string:num>', methods=['GET', 'POST'])
def dbdata(num):
  db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
  cursor = db.cursor()
  print num
  cursor.execute("SELECT hodnoty FROM  graph WHERE id=%s", num)
  rv = cursor.fetchone()
  return str(rv[0])

@app.route('/read/<string:num>')
def readmyfile(num):
    fo1515 = open("static/files/ALL.txt","r")
    rows = fo1515.readlines()
    return rows[int(num)-1]

@socketio.on('my_event', namespace='/test')
def test_message(message5):
    today=date.today()
    d1=today.strftime("%d/%m/%Y")
    session['date'] = d1

@socketio.on('db_event', namespace='/test')
def db_message(message):   
#     session['db_value'] = message['value']
    global datab
    if datab:        
        datab = 0
        print("\nLOADING DATA")        
    else:
        datab = 1
        print("\nDATA LOADED AND WRITTEN TO THE FILE AND DATABASE")

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
        today=date.today()
        x=datetime.datetime.now()
        print x.strftime("%A"),x.strftime("%d/%m/%y"),x.strftime("%X"), "\n"

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)
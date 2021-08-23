from flask import Flask, redirect, url_for, request,render_template,session
import json
import os
#from forms import ContactForm
import pymongo
from pymongo import MongoClient
from flask import flash
import shutil
import socket
import ast
import zipfile
import requests

ipPort_SensorManager = "127.0.0.1:6767"
port=5018
ip="127.0.0.1"


cluster = MongoClient("mongodb+srv://SNSTeam:1234@mycluster.wrkyk.mongodb.net/IAS_Project?retryWrites=true&w=majority")
 
db = cluster["IAS_Project"]
admin_info = db["admin_info"]
user_info = db["user_info"]
deploy_info = db["deployment_info"]

app = Flask(__name__, template_folder='template')
app.secret_key = 'development key'

#--------------------------------------------------------------------------------------------------------------------

@app.route('/register_success1')
def register_success1():
   flash('User Already Exist', 'error')
   return render_template('login.html')
   #return redirect('http://localhost:5000/login')

@app.route('/register_success2')
def register_success2():
   flash('User created successfully', 'error')
   return render_template('login.html')
   #return redirect("http://localhost:5000/login")

@app.route('/login_error1')
def login_error1():
   flash("No such id exists","error")
   #return redirect('http://localhost:5000/register')
   return render_template('register.html')

@app.route('/login_error2')
def login_error2():
   flash("Wrong password","error")
   #return redirect('http://localhost:5000/login')
   return render_template('login.html')

@app.route('/login_success1')
def login_success1():
   #flash("No such id exists","error")
   #return redirect('http://localhost:5000/admin')
   return render_template('admin.html')


@app.route('/login_success2')
def login_success2():
   #flash("No such id exists","error")
   return redirect('http://localhost:5000/user')

@app.route('/admin_success1')
def admin_success1():
   #flash("No such id exists","error")
   return render_template('admin.html')

@app.route('/admin_success2')
def admin_success2():
   #flash("No such id exists","error")
   return render_template('admin.html')

@app.route('/admin_success3')
def admin_success3():
   #flash("No such id exists","error")
   return render_template('admin.html')

@app.route('/admin_success4')
def admin_success4():
   #flash("No such id exists","error")
   return render_template('admin.html')

@app.route('/admin_success5')
def admin_success5():
   #flash("No such id exists","error")
   return render_template('admin.html')

@app.route('/admin_success6')
def admin_success6():
   #flash("No such id exists","error")
   return render_template('admin.html')

@app.route('/user_success1')
def user_success1():
   flash("Successfully started!")
   #flash("No such id exists","error")
   return render_template('admin.html')
   #return render_template('user_stop.html')

@app.route('/user_success6')
def user_success6():
   flash("Successfully stopped!")
   #return render_template('admin.html')
   return redirect('http://localhost:5000/user')


@app.route('/user_error1')
def user_error1():
   return redirect('http://localhost:5000/user')
#------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------index---------------------------------------------------------
@app.route('/',methods = ['POST', 'GET'])
def index():
   #print("fhjmfgjm")
   if request.method == 'POST':
      #print("dthjrfjsfjrtf")
      if request.form.get("login_button"):
         #print("drftjuerjt")
         return render_template('login.html')
      if request.form.get("register_button"):
         return render_template('register.html')
   
   return render_template('index.html')
#-------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------/login--------------------------------------------------------------------
@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      #print("Hello")
      user = request.form['uid']
      pswd = request.form['pswd']
      types = request.form['user_type']
      print(user,pswd,types)
      if types == "Application Admin":
         
         results = admin_info.find({"_id":user})
         flag=0
         for mp in results:
            if (flag==1 or flag==2):
               break
            if (user==mp["_id"]):
               flag=1
               if pswd==mp["password"]:
                  flag=2
                  break


         if flag==0:
            print("No such id exists")
            return redirect(url_for('login_error1'))


            
         elif flag==2:
            print("__________________Welcome "+user+"__________________")
            return redirect(url_for('login_success1'))
            
         else:
            print("Wrong password")
            return redirect(url_for('login_error2'))
      
      
      else:
         print(2)
         results = user_info.find({"_id":user})         
         flag=0
         for mp in results:
            if (flag==1 or flag==2):
               break
            if (user==mp["_id"]):
               flag=1
               if pswd==mp["password"]:
                  flag=2
                  break

         if flag==0:
            print("No such id exists")
            return redirect(url_for('login_error1'))
         elif flag==2:
            print("__________________Welcome "+user+"__________________")
            return redirect(url_for('login_success2'))
         else:
            print("Wrong password")
            return redirect(url_for('login_error2'))
#------------------------------------------------------------------------------------------------------------------------------




#----------------------------------------------------------/register--------------------------------------------------------------
@app.route('/register',methods = ['POST', 'GET'])
def register():
   if request.method == 'POST':
      print("Hello")
      user = request.form['uid']
      pswd = request.form['pswd']
      types = request.form['user_type']
      #print(user,pswd,types)
      if types == "Application Admin":
         print(1)
         mp={user:pswd}
         results = admin_info.find({"_id":user})
         flag=0
         for mp in results:
            if (user==mp["_id"]):
               flag=1

         if flag==1:
            print("User Already exists")
            #flash('User Already Exist', 'error')
            #return render_template('login.html')
            return redirect(url_for('register_success1'))
            
         else:
            admin_info.insert_one( { "_id": user, "password": pswd } )
            print("User created successfully")
            #flash('User created successfully', 'success')
            #return render_template('login.html')
            return redirect(url_for('register_success2'))
            
      else:
         print(2)
         mp={user:pswd}
            
         results = user_info.find({"_id":user})
         flag=0
         for mp in results:
            if (user==mp["_id"]):
               flag=1

         if flag==1:
            print("User Already exists")
            #flash('User Already Exist')
            #return render_template('login.html')
            return redirect(url_for('register_success1'))
         else:
            user_info.insert_one( { "_id": user, "password": pswd } )
            print("User created successfully")
            #flash('User created successfully')
            #return render_template('login.html')
            return redirect(url_for('register_success2'))
      

#------------------------------------------------------------------------------------------------------------------------------



#-----------------------------------------------------------/admin---------------------------------------------------------------
app.config['Files_upload']="./Files_upload"

@app.route('/admin',methods=['POST','GET'])
def admin():
   if request.method == 'POST':

      if request.form['admin_option'] == "Install The Sensor Class (Sensor Catalogue)":
         #print("1")
         t=request.files['myfile']
         #print(t)
         #return redirect(request.url)
         fname=request.files['myfile'].filename
         #print(fname)
         t.save(os.path.join(app.config["Files_upload"],t.filename))
         #res=t.read()
         path=app.config['Files_upload']+"/"+fname
         #print(path)
         with open(path,"r") as f:
            data=json.load(f)
         f.close()
         print(data,type (data))

         # string me convert krke bhej do socket programming ke through
         #------------------------socket programming---------------------------------

         clientfd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         clientfd.connect((ip,port))
         s="app"
         s+="*"
         s+="admin"
         s+="*"
         s+="1"
         s+="*"
         s+=str(data)
         clientfd.sendall(s.encode())
         res=clientfd.recv(50000).decode()
         #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
         #print(res,type(res))
         res=res.replace("'",'"')
         res=json.loads(res) #dict
         #print(res,type(res))
         print(res["msg"])
         m=res["msg"]
         flash(m,"error")
         clientfd.close()
         return redirect(url_for('admin_success1'))

         #------------------------socket programming khtm-------------------------------------------


      elif request.form['admin_option'] == "Install The Sensor Instance":
         #print("2")
         t=request.files['myfile']
         print(t)
         #return redirect(request.url)
         fname=request.files['myfile'].filename
         print(fname)
         t.save(os.path.join(app.config["Files_upload"],t.filename))
         #res=t.read()
         path=app.config['Files_upload']+"/"+fname
         print(path)
         with open(path,"r") as f:
            data=json.load(f)
         f.close()
         print(data,type (data))

         # string me convert krke bhej do socket programming ke through
         #------------------------socket programming---------------------------------

         clientfd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         clientfd.connect((ip,port))
         s="app"
         s+="*"
         s+="admin"
         s+="*"
         s+="2"
         s+="*"
         s+=str(data)
         clientfd.sendall(s.encode())
         res=clientfd.recv(50000).decode()
         res=res.replace("'",'"')
         lst=ast.literal_eval(res)
         #print(lst)
         for i in range(len(lst)):
            #print(type(lst[i]))
            t=json.dumps(lst[i])
            #print(t)
            t=json.loads(t)
            #print(t)
            #print(type(t))
            a=t["msg"]
            #b=t['msg']
            #print(a)
            k=i+1
            m=""
            m+="For instance "
            m+=str(k)
            m+=" --> "
            m+=a
            flash(m,"error")
            print("For instance "+str(k)+" --> "+a)
         print()
         #flash(m,"error")
         clientfd.close()
         return redirect(url_for('admin_success2'))

         #------------------------socket programming khtm-------------------------------------------
      elif request.form['admin_option'] == "Install The Barricades":
         #print("4")
         t=request.files['myfile']
         #print(t)
         #return redirect(request.url)
         fname=request.files['myfile'].filename
         #print(fname)
         t.save(os.path.join(app.config["Files_upload"],t.filename))
         #res=t.read()
         path=app.config['Files_upload']+"/"+fname
         #print(path)
         with open(path,"r") as f:
            data=json.load(f)
         f.close()
         
         #f=open(path)
         #data=json.load(f)
         #print(data,type (data))

         # string me convert krke bhej do socket programming ke through
         #------------------------socket programming---------------------------------

         clientfd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         clientfd.connect((ip,port))
         s="app"
         s+="*"
         s+="admin"
         s+="*"
         s+="4"
         s+="*"
         s+=str(data)
         clientfd.sendall(s.encode())
         res=clientfd.recv(50000).decode()
         #print()
         flash(res,"error")
         clientfd.close()
         return redirect(url_for('admin_success6'))


      elif request.form['admin_option'] == "Upload The Application":
         #print("3")
         t=request.files['myfile']
         #print(t)
         #return redirect(request.url)
         fname=request.files['myfile'].filename
         #print(fname)
         t.save(os.path.join(app.config["Files_upload"],t.filename))
         t=fname.split(".")
         #path=app.config['Files_upload']+"/"+t[0]
         path=app.config['Files_upload']
         fpath=app.config['Files_upload']+"/"+fname
         #print(fpath)
         #print("************")
         #print(path)
         path_to_zip_file=fpath
         with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(path)

         #shutil.unpack_archive(fpath,path,"zip")
         curr_loc=app.config["Files_upload"]
         for root, dirs, f in os.walk(curr_loc):
            for filename in f:
               if "application3" in filename:
                  config_file1=filename
               if "application124" in filename:
                  config_file2=filename
               
         config_path1=curr_loc +"/application3.py"
         config_path2=curr_loc +"/application124.py"
         fd1=""
         with open(config_path1,"r") as f:
            fd1+=f.read()
         f.close()
         fd2=""
         with open(config_path2,"r") as f:
            fd2+=f.read()
         f.close()
         #print(fd1)
         #print(fd2)

         #------------------------socket programming---------------------------------
         s=""
         clientfd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         clientfd.connect((ip,port))
         s="app"
         s+="*"
         s+="admin"
         s+="*"
         s+="3"
         s+="*"
         s+=str(fd1)
         s+="*"
         s+=str(fd2)
         s+="*"
         s+=str("buzzer")
         clientfd.sendall(s.encode())
         res=clientfd.recv(50000).decode()
         clientfd.close()
         """
         lst=ast.literal_eval(res)

         if False not in lst:
            #s+="The Application is deployed"
            try:
               deploy_info.insert_one( { "_id": t[0]} )
               s=""
               s+="The Application "+str(t[0])+" is deployed"
               flash(s,"error")
               return redirect(url_for('admin_success3'))
   
            except:
               s=""
               s+="The Application "+str(t[0])+" is already deployed"
               flash(s,"error")
               return redirect(url_for('admin_success4'))
         """
         s=""
         s+="The Application is deployed successfully!!"
         flash(s,"error")
               
         return redirect(url_for('admin_success3'))
         """
         else:
            s=""
            s+="The Application cannot be deployed because some of the sensors are not installed"
            flash(s,"error")
            return redirect(url_for('admin_success5'))
         """
         
         

         #------------------------socket programming khtm-------------------------------------------
      

#-------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------/user-----------------------------------------------------------------
@app.route('/user',methods=['POST','GET'])
def user():
   #form=ContactForm()
   if request.method == "POST":
      if request.method == 'GET':
         return render_template('user.html')
      else:
         #print(23)
         #print("11")
         
         selected_app=request.form["appname"]
         session['selected_app']=selected_app

         #lst=sm.bus_list()
         #lst=["Bus1","Bus2","Bus3"]
         
         ipPort_SensorManager = "127.0.0.1:6767"
         url="http://"+ipPort_SensorManager+"/getAllBusInstances"
         
         lst = requests.get(url)
         lst=ast.literal_eval(lst.text)
         
         if selected_app not in lst:
            flash("There is no such bus")
            return redirect(url_for('user_error1'))

         path2=app.config['Files_upload']+"/"+"application124.py"
         data1=""
         with open(path2,"r") as f:
            data1+=f.read()
         f.close()
         #data1=open(path2)
         

         t2=request.files['myfile2']
         #print(t2)
         #return redirect(request.url)
         fname2=request.files['myfile2'].filename
         #print(fname2)
         t2.save(os.path.join(app.config["Files_upload"],t2.filename))
         #res=t.read()
         path2=app.config['Files_upload']+"/"+fname2
         # print(path2)
         with open(path2,"r") as f2:
            data2=json.load(f2)
         f2.close()
         
         #f2=open(path2)
         """
         f2=""
         with open(path2,"r") as f:
            f2+=f.read()
         """
         #data2=json.load(f2)
         
         #------------------------socket programming---------------------------------

         clientfd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         clientfd.connect((ip,port))
         s="app"
         s+="*"
         s+="user"
         s+="*"
         s+="start"
         s+="*"
         s+=selected_app
         
         clientfd.sendall(s.encode())
        

         #s=str(data1) #application124

         #print("********data1-app124*****************")
         #print(data1,type (data1))
         i=0
         while(i<len(data1) and i+2000<len(data1)):
            print("Sending data1")
            clientfd.sendall(data1[i:i+2000].encode())
            i=i+2000

         if (i<len(data1)):
            print("Sending data1")
            clientfd.sendall(data1[i:].encode())

         clientfd.sendall("done".encode())
         res=clientfd.recv(50000).decode()         
         s=json.dumps(data2) #sensor_info
         
         #print("*************info.json ka data****************")
         #print(s,type (s))
         
         clientfd.sendall(s.encode())
         

         res=clientfd.recv(50000).decode()
         #final response recvd
         flash(res,"error")
         
         #return redirect(url_for('user_success1'))
         
         return render_template('user_stop.html', bus_name=selected_app)

         
         

 

         #####add while integrate



   elif request.method == "GET":
      return render_template('user.html')
   return "khtm"
#----------------------------------------------------------------------------------------------------------------------------------
@app.route('/user_stop',methods=['POST','GET'])
def user_stop():
   #form=ContactForm()
   if request.method == "POST":
      if request.method == 'GET':
         return render_template('user.html')
      else:
         
         #print("22")
         selected_app=session['selected_app']
         print("***")
         print(selected_app)
         clientfd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         clientfd.connect((ip,port))
         s="app"
         s+="*"
         s+="user"
         s+="*"
         s+="STOP"
         s+="*"
         s+=selected_app
         clientfd.sendall(s.encode())
         res=clientfd.recv(50000).decode()
         
         return redirect(url_for('user_success6'))




#---------------------------------------------------------/temp----------------------------------------------------------------
@app.route('/temp',methods=['POST','GET'])
def temp():
   if request.method == "POST":
      return "jdgn"

#--------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
   app.run(debug = True)
   #app.run(host='0.0.0.0',debug = True)

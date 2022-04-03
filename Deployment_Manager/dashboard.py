from flask import Flask, request, redirect
from flask import render_template
import paramiko
import threading
import time
import os
import requests

app = Flask(__name__)

username = "IASHackathon1"
password = "IASHackathon1"
hostname = "20.213.161.182"
port = 22 
appname = "test_deploy"
service_name = "s_name"

def wait(t):
    time.sleep(t)


data = {}
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('dashboard.html', authcode=None)

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if (request.method == 'POST'):
        f1 = request.files["f1"]
        f2 = request.files["f2"]
        f3 = request.files["f3"]
        data['f1'] = f1.filename
        data['f2'] = f2.filename
        data['f3'] = f3.filename
        f4 = request.files["f4"]
        f5 = request.files["f5"]
        f6 = request.files["f6"]
        data['f4'] = f4.filename
        data['f5'] = f5.filename
        data['f6'] = f6.filename
        
        #print(request.form.get('role'))
    
    print(data)
    #r = requests.post('http://127.0.0.1:5005/',json=data)
    upload_file() 

    # ///////////////// Shaon
    # t1 = threading.Thread(target=call_vm)
    # t1.start()
    call_vm()
    return "ok"
    # ////////////////
    
    #return render_template('dashboard.html', authcode=None)


def call_vm():
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Check 1")
    try:
        s.connect(hostname, port, username, password, allow_agent=True,look_for_keys = False)
    except Exception as e:
        print("Exception")
        print(e)
    print("Check 2")
    cmd_create_folder = "mkdir '"+"docker_test"+"'"
    stdin,stdout,stderr = s.exec_command(cmd_create_folder)
    print("Check 3")
    ftp_client=s.open_sftp()
    print("Check 4")
    ftp_client.put('./Dockerfile' , './docker_test/Dockerfile')
    print("Check 5")
    wait(0.5)
    ftp_client.put('./WrapperClass.py' , './docker_test/WrapperClass.py')
    print("Check 6")
    wait(0.5)
    
    buil_cmd = "sudo docker build -t test_1 'docker_test'"
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    lines = stdout.readlines()
    print(lines)
    # stdin,stdout,stderr= s.exec_command("sudo docker build . -t my-web-app -f Dockerfile")
    run_cmd = "sudo docker run --network=\"host\" test_1:latest"
    stdin,stdout,stderr= s.exec_command(run_cmd)
    lines = stdout.readlines()
    print(lines)

def upload_file():
    uploaded_file1 = request.files['f1']
    uploaded_file2 = request.files['f2']
    uploaded_file3 = request.files['f3']
    uploaded_file4 = request.files['f4']
    uploaded_file5 = request.files['f5']
    uploaded_file6 = request.files['f6']
    if uploaded_file1.filename != '':
        uploaded_file1.save(uploaded_file1.filename)
    if uploaded_file2.filename != '':
        uploaded_file2.save(uploaded_file2.filename)
    if uploaded_file3.filename != '':
        uploaded_file3.save(uploaded_file3.filename)
    if uploaded_file4.filename != '':
        uploaded_file4.save(uploaded_file4.filename)
    if uploaded_file5.filename != '':
        uploaded_file5.save(uploaded_file5.filename)
    if uploaded_file6.filename != '':
        uploaded_file6.save(uploaded_file6.filename)

    if uploaded_file1.filename != '':
        # It's data scientist
        # cmd = "./scripts/dataScientistHandeler.sh" + " " +uploaded_file3.filename + " " + uploaded_file1.filename + " " + uploaded_file2.filename
        print("calling script")
        os.system("python3 dockerFileGenerator.py " + uploaded_file3.filename)
        os.system("python3 wrapperClassGenerator.py " + uploaded_file2.filename +" "+uploaded_file1.filename)
        print("calling script")
        # os.system(cmd)
        

    else:
        # else app developer
        pass
    
    print("It's working hahaha")
	
app.run(port=5005,debug=False)
from flask import Flask, request, redirect
from flask import render_template
import paramiko
import time
import os
import requests
from pymongo import MongoClient
import load_balancer
from flask import Flask
from flask import request
from numpy import source
from pymongo import MongoClient
import os
from azure.storage.fileshare import ShareFileClient
from azure.storage.fileshare import ShareDirectoryClient
from azure.storage.fileshare import ShareClient

app = Flask(__name__)

port = 22 
appname = "test_deploy"
service_name = "s_name"

def wait(t):
    time.sleep(t)

connection_string = "DefaultEndpointsProtocol=https;AccountName=storageias;AccountKey=tnxGtqqFpuRfoJMxRR7H5evonZ0P+2dZVoV+VSTHKqOSyxkMIihIUMsXQ7KM+eLguN2/b8ncl3S9+AStZRvImg==;EndpointSuffix=core.windows.net"
file_client = ShareFileClient.from_connection_string(conn_str=connection_string,share_name="testing-file-share",file_path="uploaded_file.py")
file_client2 = ShareClient.from_connection_string(conn_str=connection_string,share_name="testing-file-share",file_path="uploaded_file.py")
share_name="testing-file-share"

def create_directory(dir_name):
    try:
        dir_client = ShareDirectoryClient.from_connection_string(connection_string, share_name, dir_name)

        print("Creating directory:", share_name + "/" + dir_name)
        dir_client.create_directory()

    except Exception as ex:
        print("ResourceExistsError:", ex)

def Upload_file_and_create_dir(folder_name,filepath):
    try:
        create_directory(folder_name)
        destination_file_path=folder_name+'/'+os.path.basename(filepath)
        print(destination_file_path)
        file_client = ShareFileClient.from_connection_string(connection_string, share_name, destination_file_path)

        with open(filepath, "rb") as source_file:
            file_client.upload_file(source_file)

        print("Succesfully Uploaded")
    except Exception as E:
        print("File_NOT_found Error")

def upload_file(folder_name,filepath):
    try:
        destination_file_path=folder_name+'/'+os.path.basename(filepath)
        print(destination_file_path)
        file_client = ShareFileClient.from_connection_string(connection_string, share_name, destination_file_path)

        with open(filepath, "rb") as source_file:
            file_client.upload_file(source_file)

        print("Succesfully Uploaded")
    except Exception as E:
        print("File_NOT_found Error")


def download_azure_file(dir_name, file_name):
    try:
        source_file_path = dir_name + "/" + file_name
        dest_file_name = file_name
        file_client = ShareFileClient.from_connection_string(connection_string, share_name, source_file_path)

        print("Downloading to:", dest_file_name)
        with open(dest_file_name, "wb") as data:
            stream = file_client.download_file()
            data.write(stream.readall())

    except Exception as ex:
        print("ResourceNotFoundError:", ex)





def download_files(folder_name):
    my_directory_client = file_client2.get_directory_client(directory_path=folder_name)
    my_list = list(my_directory_client.list_directories_and_files())
    for file in my_directory_client.list_directories_and_files():
        download_azure_file(folder_name,file["name"])
        # print(file["name"])

		# print(folder_name,file["name"])

# upload_file("nayafolder","file_share.py")







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

        CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

        client = MongoClient(CONNECTION_STRING)

        dbname = client['AI_PLATFORM']

        col1 = dbname["model_nodes"]
        col2 = dbname["app_nodes"]

        if f1.filename!='':
            if f2.filename=='' or f3.filename=='':
                return "All files not uploaded"
        if f2.filename!='':
            if f1.filename=='' or f3.filename=='':
                return "All files not uploaded"
        if f3.filename!='':
            if f1.filename=='' or f2.filename=='':
                return "All files not uploaded"
        if f4.filename!='':
            if f6.filename=='':
                return "All files not uploaded"
        if f6.filename!='':
            if f4.filename=='':
                return "All files not uploaded"
        if f1.filename=='' and f2.filename=='' and f3.filename=='' and f4.filename=='' and f5.filename=='' and f6.filename=='':
            return "No files uploaded"

        if f1.filename!='' and f1.filename[-4:]!=".pkl":
            return "Wrong type of file uploaded - pkl"
        if f2.filename!='' and f2.filename[-3:]!=".py":
            return "Wrong type of file uploaded - py"
        if f3.filename!='' and f3.filename[-5:]!=".json":
            return "Wrong type of file uploaded - json - model"
        if f4.filename!='' and f4.filename[-4:]!=".zip":
            return "Wrong type of file uploaded - zip"
        if f6.filename!='' and f6.filename[-5:]!=".json":
            return "Wrong type of file uploaded - json"


        if(f1.filename!=''):
            fname_len = len(f1.filename)
            modelName = f1.filename[0:fname_len-4]
            query = {"model":modelName}
            if(len(list(col1.find(query)))>0):
                return "Model already deployed"
        
        if(f4.filename!=''):    
            fname_len = len(f4.filename)
            appName = f4.filename[0:fname_len-4]
            query = {"app":appName}
            if(len(list(col2.find(query)))>0):
                return "App already deployed"


        
        print(request.form.get('role'))
    
    print(data)
    # r = requests.post('http://127.0.0.1:5000/',json=data)

    CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)

    dbname = client['AI_PLATFORM']

    col1 = dbname['node']
    col2 = dbname['model_nodes']

    username, password, ip = load_balancer.choose_best_node()
    print(ip)

    myquery = { "ip": ip }
    vm = col1.find(myquery)
    service_port = 0
    for i in vm:
        service_port = i["first_free_port"]
    #print(port)
    p = service_port + 1
    col1.update_one({"ip":ip},{"$set":{"first_free_port":p}})


    
    role = upload(service_port)

    if role == "application":
        zipfile = f4.filename[:-4]#to remove .zip from name of zip folder name
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # username, password, ip
        # s.connect('20.213.161.182', 22, 'IASHackathon1', 'IASHackathon1')
        s.connect(ip, 22, username, password) 
        stdin,stdout,stderr = s.exec_command('mkdir ./App;ls')
        print(1,stderr.readline(),stdout.readline())
        stdin,stdout,stderr = s.exec_command('sudo apt install unzip')
        print(22,stderr.readline(),stdout.readline())
        ftp_client=s.open_sftp()
        ftp_client.put('./'+zipfile+'.zip' , './App/'+zipfile+'.zip')
        time.sleep(0.5)
        stdin,stdout,stderr = s.exec_command('cd App;unzip '+zipfile+'.zip')
        print(333,stderr.readline(),stdout.readline())
        ftp_client.put('./Dockerfile' , './App/'+zipfile+'/Dockerfile')
        time.sleep(0.5)
        stdin,stdout,stderr = s.exec_command('sudo docker build -t '+zipfile+' ./App/'+zipfile+'/')
        print(4444,stderr.readline(),stdout.readline())
        stdin,stdout,stderr = s.exec_command('sudo docker run -p '+str(service_port)+':5000 '+zipfile+'')
        print(55555,stderr.readline(),stdout.readline())
        CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

        client = MongoClient(CONNECTION_STRING)

        dbname = client['AI_PLATFORM']

        col = dbname["app_nodes"]

        fname_len = len(f4.filename)
        appName = f4.filename[0:fname_len-4]

        data_entry = [{"ip": ip,"username": username,"password":password,"app":appName,"port":service_port}]
        for i in data_entry:
            a = col.insert_one(i)
        return "ok"
        

    
    
    # ///////////////// Shaon
    else:
        # //////////////// Ayush
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(ip, 22, username, password)
        # s.connect('20.216.24.73', 22, 'azureuser', '@mazingSpiderMan')
        # foodfood
        modelName = f1.filename[0:len(f1.filename)-4]
        stdin,stdout,stderr = s.exec_command('mkdir ./Model')
        stdin,stdout,stderr = s.exec_command('cd Model;mkdir ./'+modelName)
        print(stderr.readline(),stdout.readline())
        print("Ayush")


        ftp_client=s.open_sftp()
        print("Ayush")
        # update zipname

        ftp_client.put('./Dockerfile' , './Model/'+modelName+'/Dockerfile')
        time.sleep(0.5)
        print("Ayush")
        ftp_client.put('./WrapperClass.py' , './Model/'+modelName+'/WrapperClass.py')
        time.sleep(0.5)
        print("check1")
        ftp_client.put('./'+modelName+'.pkl' , './Model/'+modelName+'/'+modelName+'.pkl')
        time.sleep(0.5)
        print("Ayush")
        # stdin,stdout,stderr = s.exec_command('cd App')


        stdin,stdout,stderr = s.exec_command('cd Model/'+modelName+';sudo docker build . -t '+ modelName)
        # App/serviceName/app.py
        print(stderr.readline(),stdout.readline())
        stdin,stdout,stderr = s.exec_command('cd Model/'+modelName+';sudo docker run -p '+str(service_port)+':5000 '+modelName)
        print(stderr.readline(),stdout.readline())
        # run docker file
        # ////////////////
        # s = paramiko.SSHClient()
        # s.load_system_host_keys()
        # s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # print("Check 1")
        # s.connect(ip, port, username, password)
        # cmd_create_folder = "mkdir '"+"docker_test"+"'"
        # stdin,stdout,stderr = s.exec_command(cmd_create_folder)
        # ftp_client=s.open_sftp()
        # ftp_client.put('./Dockerfile' , './docker_test/Dockerfile')
        # wait(0.5)
        # ftp_client.put('./WrapperClass.py' , './docker_test/WrapperClass.py')
        # wait(0.5)
        
        # buil_cmd = "sudo docker build -t test_1 'docker_test'"
        # stdin,stdout,stderr = s.exec_command(buil_cmd)
        # lines = stdout.readlines()
        # print(lines)
        # # stdin,stdout,stderr= s.exec_command("sudo docker build . -t my-web-app -f Dockerfile")
        # run_cmd = "sudo docker run --network=\"host\" test_1:latest"
        # stdin,stdout,stderr= s.exec_command(run_cmd)
        # lines = stdout.readlines()
        # print(lines)
    # ////////////////////////
        CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

        client = MongoClient(CONNECTION_STRING)

        dbname = client['AI_PLATFORM']

        col = dbname["model_nodes"]

        fname_len = len(f1.filename)
        modelName = f1.filename[0:fname_len-4]
        data_entry = [{"ip": ip,"username": username,"password":password,"model":modelName,"port":service_port}]
        for i in data_entry:
            a = col.insert_one(i)
        return "ok"
        # ////////////////

    #return render_template('dashboard.html', authcode=None)

def upload(service_port):
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
        os.system("python3 dockerFileGenerator.py " + uploaded_file3.filename + " " + uploaded_file1.filename)
        os.system("python3 wrapperClassGenerator.py " + uploaded_file2.filename +" "+uploaded_file1.filename)
        print("calling script")
        # os.system(cmd)

        app_or_model_name  = uploaded_file1.filename[:-4]+"_model"

        Upload_file_and_create_dir(app_or_model_name,uploaded_file1.filename)
        upload_file(app_or_model_name,"WrapperClass.py")
        upload_file(app_or_model_name,"Dockerfile")

        return "model"
        

    else:
        
        os.system("python3 Application_docker_generator.py " + uploaded_file6.filename ) 

        app_or_model_name  = uploaded_file4.filename[:-4]+"_app"

        Upload_file_and_create_dir(app_or_model_name,uploaded_file4.filename)
        upload_file(app_or_model_name,"Dockerfile")      

        return "application"

# For fault tollerence - 
@app.route("/ftApp/<name>", methods=['GET', 'POST'])
def ftApp(name):
    # get zip file
    # get docker file
    download_files(name+"_app")
    zipfile = name

    username, password, ip = load_balancer.choose_best_node()

    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ip, 22, username, password) 

    stdin,stdout,stderr = s.exec_command('mkdir ./App;ls')
    print(1,stderr.readline(),stdout.readline())

    stdin,stdout,stderr = s.exec_command('sudo apt install unzip')
    print(22,stderr.readline(),stdout.readline())

    ftp_client=s.open_sftp()
    
    ftp_client.put('./'+zipfile+'.zip' , './App/'+zipfile+'.zip')
    time.sleep(0.5)

    stdin,stdout,stderr = s.exec_command('cd App;unzip '+zipfile+'.zip')
    print(333,stderr.readline(),stdout.readline())

    ftp_client.put('./Dockerfile' , './App/'+zipfile+'/Dockerfile')
    time.sleep(0.5)

    stdin,stdout,stderr = s.exec_command('sudo docker build -t '+zipfile+' ./App/'+zipfile+'/')
    print(4444,stderr.readline(),stdout.readline())
    CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)

    dbname = client['AI_PLATFORM']

    col1 = dbname['node']
    myquery = { "ip": ip }
    vm = col1.find(myquery)
    service_port = 0
    for i in vm:
        service_port = i["first_free_port"]
    #print(port)
    p = service_port + 1
    col1.update_one({"ip":ip},{"$set":{"first_free_port":p}})

    stdin,stdout,stderr = s.exec_command('sudo docker run -p '+str(service_port)+':5000 '+zipfile+'')
    print(55555,stderr.readline(),stdout.readline())

    CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    dbname = client['AI_PLATFORM']
    col = dbname["app_nodes"]
    fname_len = len(zipfile + ".zip")
    appName = zipfile
    myquery = {"app":appName}
    col.delete_one(myquery)
    data_entry = [{"ip": ip,"username": username,"password":password,"app":appName,"port":service_port}]
    for i in data_entry:
        a = col.insert_one(i)
    return "ok"

@app.route("/ftModel/<name>", methods=['GET', 'POST'])
def ftModel(name):
    # get pickle file
    # get Wrapper file
    # get dockerfile

    download_files(name+"_model")

    username, password, ip = load_balancer.choose_best_node()

    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ip, 22, username, password)
    
    modelName = name # without .pkl
    stdin,stdout,stderr = s.exec_command('mkdir ./Model')
    stdin,stdout,stderr = s.exec_command('cd Model;mkdir ./'+modelName)

    ftp_client=s.open_sftp()

    ftp_client.put('./Dockerfile' , './Model/'+modelName+'/Dockerfile')
    time.sleep(0.5)
    ftp_client.put('./WrapperClass.py' , './Model/'+modelName+'/WrapperClass.py')
    time.sleep(0.5)
    ftp_client.put('./'+modelName+'.pkl' , './Model/'+modelName+'/'+modelName+'.pkl')
    time.sleep(0.5)
    # stdin,stdout,stderr = s.exec_command('cd App')

    CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)

    dbname = client['AI_PLATFORM']

    col1 = dbname['node']
    myquery = { "ip": ip }
    vm = col1.find(myquery)
    service_port = 0
    for i in vm:
        service_port = i["first_free_port"]
    #print(port)
    p = service_port + 1
    col1.update_one({"ip":ip},{"$set":{"first_free_port":p}})

    col2 = dbname["model_nodes"]
    myquery = {"model":modelName}
    col2.delete_one(myquery)
    data_entry = [{"ip": ip,"username": username,"password":password,"model":modelName,"port":service_port}]
    for i in data_entry:
        a = col2.insert_one(i)
    
    stdin,stdout,stderr = s.exec_command('cd Model/'+modelName+';sudo docker build . -t '+ modelName)
    # App/serviceName/app.py
    print(stderr.readline(),stdout.readline())

    stdin,stdout,stderr = s.exec_command('cd Model/'+modelName+';sudo docker run -p '+str(service_port)+':5000 '+modelName)
    print(stderr.readline(),stdout.readline())

    return "ok"
    

    
app.run()
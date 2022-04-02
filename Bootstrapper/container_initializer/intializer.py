import paramiko
import json
import os

f1 = open('./Bootstrapper/vm_user_config.json')
vm_user = json.load(f1)
f2 = open('./Bootstrapper/vm_details.json')
vm_details = json.load(f2)
f3 = open('./Bootstrapper/container_initializer/initializer_config.json')
initialize_details = json.load(f3)

UU= "iasVM1234568"
ip = "20.219.122.194"

def initialize_docker_env(vm_name):
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(vm_details[vm_name]['ip'], 22, vm_user["username"], vm_user["password"])

    build_cmd = "curl -fsSL https://get.docker.com -o get-docker.sh"
    stdin,stdout,stderr = s.exec_command(build_cmd)
    lines = stdout.readlines()
    print(lines)

    buil_cmd = "sh get-docker.sh"
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    lines = stdout.readlines()
    print(lines)

    buil_cmd = "curl -fsSL https://test.docker.com -o test-docker.sh"
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    lines = stdout.readlines()
    print(lines)

    buil_cmd = "sh test-docker.sh" 
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    lines = stdout.readlines()
    print(lines)
    
    buil_cmd = "sh install.sh" 
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    lines = stdout.readlines()
    print(lines)

    buil_cmd = "docker -v" 
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    lines = stdout.readlines()
    print(lines)


def upload_container(service_name,vm_name,source,destination):
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #client.connect("20.213.161.182", 22, "IASHackathon1", "IASHackathon1")
    client.connect(vm_details[vm_name]['ip'], 22, vm_user["username"], vm_user["password"])
    sftp_client=client.open_sftp()

    localfolder=source
    basefolder=destination

    for path,dirs,files in os.walk(localfolder):
        if path.lstrip(localfolder)!=None:       
            extrapath=path.split(basefolder)[-1]   
            command="cd root"  
            stdin,stdout,stderr = client.exec_command(command)
            command="mkdir {}".format(extrapath)
            client.exec_command(command)
            lines = stdout.readlines()   
            print(lines)
            
        for file in files:  
            filepath=os.path.join(path,file)
            extrapath=path.split(basefolder)[-1]
            command="cd root"  
            stdin,stdout,stderr = client.exec_command(command)
            sftp_client.put(filepath,"{}/{}".format(extrapath,file))

    sftp_client.close()
    client.close()

def initialize_container(service_name,port,vm_name,source,destination):
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #s.connect("20.213.161.182", 22, "IASHackathon1", "IASHackathon1")
    s.connect(vm_details[vm_name]['ip'], 22, vm_user["username"], vm_user["password"])
    
    # # buil_cmd = "ls" 
    # # stdin,stdout,stderr = s.exec_command(buil_cmd)
    # # lines = stdout.readlines()
    # # print(lines)

    buil_cmd = "sudo systemctl start docker" 
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    lines = stdout.readlines()
    print(lines)

    buil_cmd = "sudo systemctl enable docker" 
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    lines = stdout.readlines()
    print(lines)

    buil_cmd = "sudo systemctl status docker" 
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    lines = stdout.readlines()
    print(lines)

    buil_cmd = "sudo docker info" 
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    lines = stdout.readlines()
    print(lines)
    # print("=====================")
    buil_cmd = "sudo docker build -t "+ service_name.lower() + " " + destination
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    lines = stdout.readlines()
    print(lines)

def start_container(service_name,port,vm_name,source,destination):
    run_cmd = "sudo docker run -p "+ str(port)+":5000 "+ service_name.lower()
    stdin,stdout,stderr= s.exec_command(run_cmd)
    lines = stdout.readlines()
    print(lines)


# for key in initialize_details:
initialize_docker_env("VM2")
upload_container("Authentication_Manager",5001, "VM2","./Authentication_Manager/","~/Authentication_Manager/")
initialize_container("Authentication_Manager",5001, "VM2","./Authentication_Manager/","~/Authentication_Manager/")
start_container("Authentication_Manager",5001, "VM2","./Authentication_Manager/","~/Authentication_Manager/")
#upload_container("Request_Manager",5000, "VM2","./Request_Manager/","~/Request_Manager/")
#initialize_containers("Request_Manager",5000, "VM1","./Request_Manager/","~/Request_Manager/")

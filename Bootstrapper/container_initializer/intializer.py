import paramiko
import json
import os

f1 = open('./Bootstrapper/vm_user_config.json')
vm_user = json.load(f1)
f2 = open('./Bootstrapper/vm_details.json')
vm_details = json.load(f2)
f3 = open('./Bootstrapper/container_initializer/initializer_config.json')
initialize_details = json.load(f3)



class MySFTPClient(paramiko.SFTPClient):
    def put_dir(self, source, target):
        ''' Uploads the contents of the source directory to the target path. The
            target directory needs to exists. All subdirectories in source are 
            created under target.
        '''
        for item in os.listdir(source):
            if os.path.isfile(os.path.join(source, item)):
                self.put(os.path.join(source, item), '%s/%s' % (target, item))
            else:
                self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                self.put_dir(os.path.join(source, item), '%s/%s' % (target, item))

    def mkdir(self, path, mode=511, ignore_existing=False):
        ''' Augments mkdir by adding an option to not fail if the folder exists  '''
        try:
            super(MySFTPClient, self).mkdir(path, mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise

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

    #client.exec_command("cd") 
    # LETS make 'aaaa' folder sync with server 
    #/root/ is home for remote server 

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
    # transport = paramiko.Transport((vm_details[vm_name]['ip'], 22))
    # transport.connect(username=vm_user["username"], password=vm_user["password"])
    # sftp = MySFTPClient.from_transport(transport)
    # sftp.mkdir(destination, ignore_existing=True)
    # sftp.put_dir(source, destination)
    # sftp.close()

    #initialize_containers(service_name,vm_name,source,destination);
    
def initialize_containers(service_name,vm_name,source,destination):
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #s.connect("20.213.161.182", 22, "IASHackathon1", "IASHackathon1")
    s.connect(vm_details[vm_name]['ip'], 22, vm_user["username"], vm_user["password"])
    
    buil_cmd = "ls" 
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    lines = stdout.readlines()
    print(lines)

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
    print("=====================")
    buil_cmd = "sudo docker build -t req_m " + service_name
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    lines = stdout.readlines()
    print(lines)
    
    # run_cmd = "cd "+destination + ";ls; sudo docker run --network=\"host\" Request_Manager ."
    # stdin,stdout,stderr= s.exec_command(run_cmd)
    # lines = stdout.readlines()
    # print(lines)
    

# for key in initialize_details:
#upload_container("Authentication_Manager", "VM1","./Authentication_Manager/","root/Authentication_Manager/")
initialize_containers("Request_Manager", "VM1","./Authentication_Manager/","root/Authentication_Manager/")
s = paramiko.SSHClient()
s.load_system_host_keys()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
s.connect(vm_details["VM1"]['ip'], 22, vm_user["username"], vm_user["password"])
build_cmd = "sudo docker images"
stdin,stdout,stderr = s.exec_command(build_cmd)
lines = stdout.readlines()
print(lines)

# buil_cmd = "ls"
# stdin,stdout,stderr = s.exec_command(buil_cmd)
# lines = stdout.readlines()
# print(lines)

# buil_cmd = "curl -fsSL https://test.docker.com -o test-docker.sh"
# stdin,stdout,stderr = s.exec_command(buil_cmd)
# lines = stdout.readlines()
# print(lines)

# buil_cmd = "sh test-docker.sh" 
# stdin,stdout,stderr = s.exec_command(buil_cmd)
# lines = stdout.readlines()
# print(lines)

# buil_cmd = "sh install.sh" 
# stdin,stdout,stderr = s.exec_command(buil_cmd)
# lines = stdout.readlines()
# print(lines)

# buil_cmd = "docker -v" 
# stdin,stdout,stderr = s.exec_command(buil_cmd)
# lines = stdout.readlines()
# print(lines)
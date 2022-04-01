import paramiko
import json
import os

f1 = open('../vm_user_config.json')
vm_user = json.load(f1)
f2 = open('../vm_details.json')
vm_details = json.load(f2)
f3 = open('./initializer_config.json')
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

def initialize_vm(service_name,vm_name,source,destination):
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    s.connect(vm_details[vm_name]['ip'], 22, vm_user["username"], vm_user["password"])
    ftp_client=s.open_sftp()
    sftp = MySFTPClient(ftp_client)
    sftp.mkdir(destination, ignore_existing=True)
    sftp.put_dir(source, destination)
    buil_cmd = "cd " + destination 
    buil_cmd = "echo hello " + destination 
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    buil_cmd = "sudo docker build -t " + service_name + " . "
    stdin,stdout,stderr = s.exec_command(buil_cmd)
    lines = stdout.readlines()
    print(lines)
    # sftp.close()

# for key in initialize_details:
initialize_vm("reque", "VM1","Ds","ds")
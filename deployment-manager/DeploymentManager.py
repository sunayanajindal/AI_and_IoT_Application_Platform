import paramiko
import time
from flask import Flask

app = Flask(__name__)

username = "IASHackathon1"
password = "IASHackathon1"
hostname = "20.213.161.182"
port = 22 
appname = "test_deploy"
service_name = "s_name"

def wait(t):
    time.sleep(t)

@app.route('/deploymentManager/deploy')
def deploy():
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname, port, username, password)
    cmd_create_folder = "mkdir '"+"docker_test"+"'"
    stdin,stdout,stderr = s.exec_command(cmd_create_folder)
    ftp_client=s.open_sftp()
    ftp_client.put('./Dockerfile' , './docker_test/Dockerfile')
    wait(0.5)
    ftp_client.put('./WrapperClass.py' , './docker_test/WrapperClass.py')
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
    return "DONE"


if __name__ == '__main__':
    app.run(debug=True)


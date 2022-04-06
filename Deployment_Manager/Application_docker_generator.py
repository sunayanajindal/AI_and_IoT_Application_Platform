import json
import sys

def dockerGenerator(config_file_path, service_name):
    configFile = open(config_file_path,'r')
    config = json.load(configFile)
    configFile.close()

    df = open('Dockerfile','w')
    print("inside docker generation")

    str = "FROM python:3\nCOPY . /app\nWORKDIR /app\n"


    all_services = config['Application']['services']

    for key,service in all_services.items():
        
        if service['servicename'] == service_name:
            dependencies = service['dependencies']#list
            filenames = service['filenames']#list



            # for ev_key,ev_val in service['environment'].items():
            #     if ev_val:
            #         if ev_key == 'flask':
            #             str += 'RUN pip3 install flask\n\n'





                    # to-do for more tech
            # entry_point = config['Application']['entryPoint']#string
    

    for dependency in dependencies:
        str += "RUN pip3 install " + dependency + "\n"

    # for filename in filenames:
    #     str += "ADD " + filename + " .\n"
    
    
    str+='CMD ["python3","-m","flask","run","--host=0.0.0.0"]'

    df.write(str)
    df.close()

# config file, service name
dockerGenerator(sys.argv[1],"service-1")

# dockerGenerator("./config.json","service-1")
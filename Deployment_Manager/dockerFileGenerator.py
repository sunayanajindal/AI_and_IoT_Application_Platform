import json
import sys
# its for models
def dockerGenerator(config_file_path, service_name, modelName):
    configFile = open(config_file_path,'r')
    config = json.load(configFile)
    configFile.close()

    df = open('Dockerfile','w')
    print("inside docker generation")

    str = "FROM ubuntu:20.04\nRUN apt-get update\nRUN apt-get install -y python3-pip\n"


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
    
    # str += "EXPOSE " + port + "\n"

    for dependency in dependencies:
        str += "RUN pip3 install " + dependency + "\n"

    # for filename in filenames:
    #     str += "ADD " + filename + " .\n"

    str += "COPY WrapperClass.py /\nCOPY "+modelName+" /\n"
        
    
    str+="CMD python3 WrapperClass.py"

    df.write(str)
    df.close()

# config file, service name
dockerGenerator(sys.argv[1],"service-1",sys.argv[2])

# dockerGenerator("./config.json","service-1")
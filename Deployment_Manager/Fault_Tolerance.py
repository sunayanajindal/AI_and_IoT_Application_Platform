
from flask import Flask
from flask import request
from numpy import source
from pymongo import MongoClient
import os
from azure.storage.fileshare import ShareFileClient
from azure.storage.fileshare import ShareDirectoryClient
from azure.storage.fileshare import ShareClient



connection_string = "DefaultEndpointsProtocol=https;AccountName=storageias;AccountKey=tnxGtqqFpuRfoJMxRR7H5evonZ0P+2dZVoV+VSTHKqOSyxkMIihIUMsXQ7KM+eLguN2/b8ncl3S9+AStZRvImg==;EndpointSuffix=core.windows.net"
file_client = ShareFileClient.from_connection_string(conn_str=connection_string,share_name="testing-file-share",file_path="uploaded_file.py")
share_name="testing-file-share"


app = Flask(__name__)

# connection_string= "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
# global_database_name ="IAS_FINAL_DATABASE"
# table_name_of_apps="Applications"


def download_azure_file(dir_name, file_name):
    try:
        source_file_path = dir_name + "/" + file_name
        dest_file_name = "DOWNLOADED-" + file_name
        file_client = ShareClient.from_connection_string(connection_string, share_name, source_file_path)

        print("Downloading to:", dest_file_name)
        with open(dest_file_name, "wb") as data:
            stream = file_client.download_file()
            data.write(stream.readall())

    except ResourceNotFoundError as ex:
        print("ResourceNotFoundError:", ex.message)





def download_files(folder_name):

	my_directory_client = file_client.get_directory_client(directory_path=folder_name)

	my_list = list(my_directory_client.list_directories_and_files())

	for file in my_directory_client.list_directories_and_files():

    	# print(file["name"])

		print(folder_name,file["name"])
		# download_azure_file(folder_name,file["name"])


@app.route('/faulttolerance')
def fault_tau():
	if(request.method=='POST'):

		data = request.get_json()

		app_or_model=data["type"]
		name=data["name"]


		# ip=data["ip"]
		# port=data["port"]

		# if(app_or_model=="app"):
		# 	client = MongoClient(connection_string)
		# 	database_name=global_database_name
		# 	monitoring_db=client[database_name]
		# 	collection_name=table_name_of_apps
		# 	app=monitoring_db[collection_name]
			
		# 	path = app.find({"name":name},{ path: 1, "_id": 0 })

		download_files(name)

			# Redeploy code here






# def create_directory(dir_name):
#     try:
#         # Create a ShareDirectoryClient from a connection string
#         dir_client = ShareDirectoryClient.from_connection_string(connection_string, share_name, dir_name)

#         print("Creating directory:", share_name + "/" + dir_name)
#         dir_client.create_directory()

#     except EXCEPTION as ex:
#         print("ResourceExistsError:", ex.message)

# def uplaod_file(folder_name,filepath):
	

# 	try:
# 		source_file=open(filepath)
# 		source_file_data=source_file.read()

# 		# Create a dir here
# 		create_directory(folder_name)

# 		destination_file_path=folder_name


# 		file_client = ShareFileClient.from_connection_string(connection_string, share_name, destination_file_path)
# 		file_client.upload_file(source_file_data)

# 	except Exception as E:
# 		print("File_NOT_found Error")






def create_directory(dir_name):
    try:
        dir_client = ShareDirectoryClient.from_connection_string(connection_string, share_name, dir_name)

        print("Creating directory:", share_name + "/" + dir_name)
        dir_client.create_directory()

    except Exception as ex:
        print("ResourceExistsError:", ex.message)

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

# upload_file("nayafolder","file_share.py")


download_files("model1_model")


@app.route('/upload')
def fault_tau():

	app_or_model_name=""
	filepath1=""
	filepath2=""
	filepath3=""

	Upload_file_and_create_dir(app_or_model_name,filepath1)
	upload_file(app_or_model_name,filepath2)
	upload_file(app_or_model_name,filepath3)



	pass




		
		



			
	


	





if __name__ == '__main__':
	app.run()


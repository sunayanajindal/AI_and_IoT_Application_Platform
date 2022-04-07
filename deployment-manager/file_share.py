# from datetime import datetime, timedelta
# from azure.storage.fileshare import ShareServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions

# sas_token = generate_account_sas(
#     account_name="<storage-account-name>",
#     account_key="<account-access-key>",
#     resource_types=ResourceTypes(service=True),
#     permission=AccountSasPermissions(read=True),
#     expiry=datetime.utcnow() + timedelta(hours=1)
# )

# share_service_client = ShareServiceClient(account_url="https://<my_account_name>.file.core.windows.net", credential=sas_token)

from distutils.command.upload import upload
from logging import exception
import os
from tkinter import EXCEPTION
from unicodedata import name

# from azure.storage.fileshare import ShareServiceClient
from azure.storage.fileshare import ShareFileClient
from azure.storage.fileshare import ShareDirectoryClient
from azure.storage.fileshare import ShareClient

connection_string = "DefaultEndpointsProtocol=https;AccountName=storageias;AccountKey=tnxGtqqFpuRfoJMxRR7H5evonZ0P+2dZVoV+VSTHKqOSyxkMIihIUMsXQ7KM+eLguN2/b8ncl3S9+AStZRvImg==;EndpointSuffix=core.windows.net"
# file_client = ShareFileClient.from_connection_string(conn_str=connection_string,share_name="testing-file-share",file_path="fault_toule.py")


# with open("./fault_toule.py", "rb") as source_file:
#     file_client.upload_file(source_file)

# with open("1final.cpp", "wb") as file_handle:
#     data = file_client.download_file()
#     data.readinto(file_handle)




# Downloading a folder example

# my_directory = file_client.get_directory_client(directory_path="Aman_folder")

# dir_client = ShareDirectoryClient.from_connection_string(conn_str=connection_string,share_name="testing-file-share",directory_path="./Aman_folder")

# for file in dir_client.list_directories_and_files():
#     # print(file["name"])

#     path = os.path.join("Aman_folder",file["name"])
#     # print(path)

#     with open(path, "wb") as file_handle:
#         data = file_client.download_file()
#         data.readinto(file_handle)
# print("success")


# my_list = list(dir_client.list_directories_and_files())

# print(my_list)


# End of the Example

# Download File from folder again example

# share = ShareClient.from_connection_string(connection_string, "testing-file-share")
# my_directory = share.get_directory_client(directory_path="Aman_folder")
# my_list = list(my_directory.list_directories_and_files())

# aaa=my_directory.directory_path()
# print(aaa)

# print(my_list)

# End of it 


# # ######################################


# def download_azure_file(connection_string, share_name, dir_name, file_name):
#     try:
#         # Build the remote path
#         source_file_path = dir_name + "/" + file_name

#         # Add a prefix to the filename to 
#         # distinguish it from the uploaded file
#         dest_file_name = "DOWNLOADED-" + file_name

#         # Create a ShareFileClient from a connection string
#         file_client = ShareFileClient.from_connection_string(
#             connection_string, share_name, source_file_path)

#         print("Downloading to:", dest_file_name)

#         # Open a file for writing bytes on the local system
#         with open(dest_file_name, "wb") as data:
#             # Download the file from Azure into a stream
#             stream = file_client.download_file()
#             # Write the stream to the local file
#             data.write(stream.readall())

#     except ResourceNotFoundError as ex:
#         print("ResourceNotFoundError:", ex.message)


# download_azure_file(connection_string,"testing-file-share","Aman_folder","2new.cpp")

# ###############################









# # To upload a folder ...... Sample code 
#  path_remove = "F:\\"
#     local_path = "F:\\folderA"

#     for r,d,f in os.walk(local_path):        
#         if f:
#             for file in f:
#                 file_path_on_azure = os.path.join(r,file).replace(path_remove,"")
#                 file_path_on_local = os.path.join(r,file)
#                 block_blob_service.create_blob_from_path(container_name,file_path_on_azure,file_path_on_local)    


# Need some changes......................
# 



#         

connection_string = "DefaultEndpointsProtocol=https;AccountName=storageias;AccountKey=tnxGtqqFpuRfoJMxRR7H5evonZ0P+2dZVoV+VSTHKqOSyxkMIihIUMsXQ7KM+eLguN2/b8ncl3S9+AStZRvImg==;EndpointSuffix=core.windows.net"
file_client = ShareClient.from_connection_string(conn_str=connection_string,share_name="testing-file-share",file_path="uploaded_file.py")
share_name="testing-file-share"



def download_azure_file(dir_name, file_name):
    try:
        # Build the remote path
        source_file_path = dir_name + "/" + file_name

        # Add a prefix to the filename to 
        # distinguish it from the uploaded file
        dest_file_name = "DOWNLOADED-" + file_name

        # Create a ShareFileClient from a connection string
        file_client = ShareFileClient.from_connection_string(
            connection_string, share_name, source_file_path)

        print("Downloading to:", dest_file_name)

        # Open a file for writing bytes on the local system
        with open(dest_file_name, "wb") as data:
            # Download the file from Azure into a stream
            stream = file_client.download_file()
            # Write the stream to the local file
            data.write(stream.readall())

    except ResourceNotFoundError as ex:
        print("ResourceNotFoundError:", ex.message)

def download_files(folder_name):

	my_directory_client = file_client.get_directory_client(directory_path=folder_name)

	my_list = list(my_directory_client.list_directories_and_files())

	for file in my_directory_client.list_directories_and_files():

    	# print(file["name"])

		# print(folder_name,file["name"])
		download_azure_file(folder_name,file["name"])

download_files('model1_model')


# def create_directory(dir_name):
#     try:
#         # Create a ShareDirectoryClient from a connection string
#         dir_client = ShareDirectoryClient.from_connection_string(connection_string, share_name, dir_name)

#         print("Creating directory:", share_name + "/" + dir_name)
#         dir_client.create_directory()

#     except EXCEPTION as ex:
#         print("ResourceExistsError:", ex.message)


# def upload_local_file(connection_string, local_file_path, share_name, dest_file_path):

    # share = ShareClient.from_connection_string(connection_string, share_name, local_file_path)
    # my_directory = share.get_directory_client(directory_path="Newdir")
    # my_directory.create_directory()

    # create_directory("New_dir")




    # dest_file_path="Aman_folder"+'/'+dest_file_path
    
    # source_file = open(local_file_path, "rb")
    # data = source_file.read()
    # # Create a ShareFileClient from a connection string
    # file_client = ShareFileClient.from_connection_string(
    #     connection_string, share_name, dest_file_path)
    # print("Uploading to:", share_name + "/" + dest_file_path)
    # file_client.upload_file(data)

    # except ResourceExistsError as ex:
    #     print("ResourceExistsError:", ex.message)

    # except ResourceNotFoundError as ex:
    #     print("ResourceNotFoundError:", ex.message)
    

# upload_local_file(connection_string,"fault_toule.py",share_name,"ThisisDocker")








# def create_directory(dir_name):
#     try:
#         # Create a ShareDirectoryClient from a connection string
#         dir_client = ShareDirectoryClient.from_connection_string(connection_string, share_name, dir_name)

#         print("Creating directory:", share_name + "/" + dir_name)
#         dir_client.create_directory()

#     except EXCEPTION as ex:
#         print("ResourceExistsError:", ex.message)

# def upload_file1(folder_name,filepath):
#     try:
#         create_directory(folder_name)
#         destination_file_path=folder_name+'/'+os.path.basename(filepath)
#         print(destination_file_path)
#         file_client = ShareFileClient.from_connection_string(connection_string, share_name, destination_file_path)

#         with open(filepath, "rb") as source_file:
#             file_client.upload_file(source_file)

#         print("Succesfully Uploaded")
#     except Exception as E:
#         print("File_NOT_found Error")

# def upload_file2(folder_name,filepath):
#     try:
#         destination_file_path=folder_name+'/'+os.path.basename(filepath)
#         print(destination_file_path)
#         file_client = ShareFileClient.from_connection_string(connection_string, share_name, destination_file_path)

#         with open(filepath, "rb") as source_file:
#             file_client.upload_file(source_file)

#         print("Succesfully Uploaded")
#     except Exception as E:
#         print("File_NOT_found Error")


# upload_file1("ekaurfolder","file_share.py")
# upload_file2("ekaurfolder","monitoring.py")
# upload_file2("ekaurfolder","uploaded_file.py")
# reate_directory(folder_name)




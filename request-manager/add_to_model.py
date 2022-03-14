from distutils.command.config import config
from flask import render_template
import requests
import json
import socket



username="xyz"

to_send={}
username = "aman3"
model_name = "model2"
to_send["username"]=username
to_send["model_name"]=model_name
response=requests.post('http://localhost:1237/add_model',json=to_send).content

# to_send={}
# username = "aman3"
# to_send["username"]=username
# response=requests.post('http://localhost:1237/get_models',json=to_send).content

# print(response.decode().split())







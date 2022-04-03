from concurrent.futures import process
from re import template
import certifi
import ast
from pymongo import MongoClient
from flask import Flask, render_template, request,redirect
from sensor_binder import *
import requests

app = Flask(__name__)

CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
REQUEST_MANAGER =  'http://127.0.0.1:5000'
SCHEDULER = "http://127.0.0.1:5011"
dbname = client['AI_PLATFORM']
app_req_db = dbname["app_requirement"]

given_app_id = "app1"
app_sensor_data = {}
sensor_kinds = list()
sensor_count = list()

def get_sensors():
    app_instance = list(app_req_db.find({"app_id" : given_app_id}))

    if app_instance == {}:
        print("Error : App ID not found")
    else:
        # print("Application sensor requirements are : ")
        sensor_req = app_instance[0]["sensors"]
        # print(sensor_req)
 
    app_sensor_req = ast.literal_eval(sensor_req)

    for  sensor_type in app_sensor_req:
        sensor_kinds.append(sensor_type)
        sensor_count.append(app_sensor_req[sensor_type])
    
    return app_sensor_req

@app.route("/jsonifyRequest", methods=['POST', 'GET'])
def sensor_requirements():
    auth_token = request.cookies.get('auth_token')
    request_details = {"info" : list()}
    new_sensor_instance = request.form.to_dict()
    # print(new_sensor_instance)
    for each in new_sensor_instance:
        l = each.split('_')
        # print (l)
        val = {"type" : l[0] , "location" : new_sensor_instance[each]}
        request_details["info"].append(val)

    # print(request_details)
    #SCHEDULER = new_sensor_instance["SCHEDULER"]
    binding_map = processRequest(request_details)
    scheduling_data = {"app_id": given_app_id,"info" : binding_map}
    # print(scheduling_data)s
    response=requests.post( SCHEDULER+ "/schedule_data",json=scheduling_data).content.decode()
   
    
    redir = redirect(REQUEST_MANAGER+"/Schedule/")
    redir.headers['Authorization'] = auth_token
    return redir


@app.route("/")
def m():
    get_sensors()
    return render_template("sensor_location.html", sensor_kinds = sensor_kinds, sensor_count=sensor_count)

app.run(port=6005)
from types import new_class
from kafka import KafkaProducer
from pymongo import MongoClient
import os
import threading
from flask import Flask, request, render_template, redirect
import random
import json
import string
import time
import schedule
from sensor_simulator import *

SENSOR_CONFIGURER = "http://127.0.0.1:6001"
REQUEST_MANAGER = 'http://127.0.0.1:5000'

CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
dbname = client['AI_PLATFORM']
IP_ADDRESSES = dbname["IP_ADDRESSES"]


ip_table = list(IP_ADDRESSES.find())
for i in ip_table:
    if 'REQUEST_MANAGER' in i:
        REQUEST_MANAGER = i['REQUEST_MANAGER']
    if 'SENSOR_CONFIGURER' in i:
        SENSOR_CONFIGURER = i['SENSOR_CONFIGURER']


CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
dbname = client['AI_PLATFORM']
SENSOR_INSTANCES_DB = dbname["SENSOR_INSTANCES"]
SENSOR_INFO_DB = dbname["SENSOR_INFO"]
app = Flask(__name__)

@app.route("/new_instance", methods=["POST", "GET"])
def configureNewSensorInstance():
    new_sensor_instance = request.form.to_dict()
    print(new_sensor_instance)
    sensor_instances = list(SENSOR_INSTANCES_DB.find())

    for instance in sensor_instances:
        temp = instance
        del temp['_id']
        if(temp == new_sensor_instance):
            print("Error: Sensor Instance is already configured.")
            redir = redirect(REQUEST_MANAGER+"/Dashboard/Platform_Configurer")
            redir.headers['Authorization'] = new_sensor_instance['token']
            return redir

    _id = SENSOR_INSTANCES_DB.insert_one(new_sensor_instance).inserted_id
    d = list(SENSOR_INFO_DB.find({"type" : new_sensor_instance['type']}))[0]
    data_format = d['input_format']
    data_rate = d['data_rate']
    
    print(data_rate)
    print("New Sensor Instance has been configured")
    schedule.every(int(data_rate)).seconds.do(produce,_id,data_format)
    redir = redirect(REQUEST_MANAGER+"/Dashboard/Platform_Configurer")
    redir.headers['Authorization'] = new_sensor_instance['token']
    return redir
    


@app.route("/new_type", methods=["POST", "GET"])
def configureNewSensorType():
    new_sensor_type = request.form.to_dict()
    print(request.form)
    sensor_types = list(SENSOR_INFO_DB.find())

    for type in sensor_types:
        temp = type
        del temp['_id']
        if(temp == new_sensor_type):
            print("Error: Sensor Type is already configured.")
            redir = redirect(REQUEST_MANAGER+"/Dashboard/Platform_Configurer")
            redir.headers['Authorization'] = new_sensor_type['token']
            return redir

    a = SENSOR_INFO_DB.insert_one(new_sensor_type)
    print("New Sensor Type confiugured")
    redir = redirect(REQUEST_MANAGER+"/Dashboard/Platform_Configurer")
    redir.headers['Authorization'] = new_sensor_type['token']
    return redir


# app.run(port=5001)

def runPending():
    # pick task from DB and run it
    print("In Run Pending")
    while True:
        schedule.run_pending()
        time.sleep(1)


def renderUI():
    app.use_reloader=False
    app.run(port=6001)

t1 = threading.Thread(target=renderUI)
t2 = threading.Thread(target = runPending)

t1.start()
t2.start()

t1.join()
t2.join()
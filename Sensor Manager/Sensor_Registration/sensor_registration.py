from kafka import KafkaConsumer
from pymongo import MongoClient
import os
from flask import Flask, request, render_template

CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
dbname = client['sensor']
SENSOR_INSTANCES_DB = dbname["SENSOR_INSTANCES"]
SENSOR_INFO_DB = dbname["SENSOR_INFO"]
app = Flask(__name__)


@app.route("/new_instance", methods=["POST", "GET"])
def configureNewSensorInstance():
    new_sensor_instance = request.form.to_dict()
    sensor_instances = list(SENSOR_INSTANCES_DB.find())

    for instance in sensor_instances:
        temp = instance
        del temp['_id']
        if(temp == new_sensor_instance):
            print("Error: Sensor Instance is already configured.")
            return render_template("configurer.html")

    SENSOR_INSTANCES_DB.insert_one(new_sensor_instance)
    print("New Sensor Instance has been configured")
    return render_template("configurer.html")


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
            return render_template("configurer.html")

    a = SENSOR_INFO_DB.insert_one(new_sensor_type)
    print("New Sensor Type confiugured")
    return render_template("configurer.html")


app.run(port=5001)

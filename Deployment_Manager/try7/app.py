from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route("/<name>",methods=['GET'])
def fun(name):
    return "Hi " + name
    
@app.route("/11",methods=['GET'])
def fun1():
    return "Team Sche"

if __name__ == "__main__":
    app.run()

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager, login_user, logout_user, login_required, UserMixin
import requests

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')


@app.route('/role',methods = ['POST', 'GET'])
def role():
    if (request.method == 'POST'):
        rol = request.form['role']
        if(rol=='Data Scientist'):

          return render_template('dem.html')
          
          user=input("Please Enter Your Username: ")
          password=(input("Enter Password: "))
          if(isvalid(user,password)):
              username=user
              do_operations()
          else:
              print("Please Try again Username or password is not valid")
    
        else:
            return render_template('dema.html')


@app.route('/signup_DS', methods = ['GET', 'POST'])
def signin():
    username=request.form['username']
    password=request.form['password']
    # data = request.get_json()
    # print("data got = ",data)
    response=requests.post('http://localhost:5000/add_user_DS',json={'username':username,'password':password}).content
    if(response.decode()=="ok"):
        return render_template("index.html")
    else:
        return "Error"
    


@app.route('/login_DS', methods = ['GET', 'POST'])
def login():
    if(request.method=='POST'): 
        username=request.form['username']
        password=request.form['password']
        # data = request.get_json()
        response=requests.post('http://localhost:5000/authen_DS',json={'username':username,'password':password}).content.decode()
        if(response=="ok"):
            return "ok"
        else:
            return "Error"

@app.route('/signup_AD', methods = ['GET', 'POST'])
def signup():
    # data = request.get_json()
    username=request.form['username']
    password=request.form['password']
    # print("data got = ",data)
    response=requests.post('http://localhost:5000/add_user_AD',json={'username':username,'password':password}).content
    if(response.decode()=="ok"):
        return render_template("index.html")
    else:
        return "Error"


@app.route('/login_AD', methods = ['GET', 'POST'])
def logup():
    if(request.method=='POST'): 
        # data = request.get_json()
        username=request.form['username']
        password=request.form['password']
        response=requests.post('http://localhost:5000/authen_AD',json={'username':username,'password':password}).content.decode()
        if(response=="ok"):
            return "ok"
        else:
            return "Error"

if(__name__ == '__main__'):
    app.run(port=1234,debug=True)


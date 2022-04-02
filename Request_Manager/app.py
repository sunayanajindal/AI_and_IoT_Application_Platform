from flask import Flask, session, request, render_template, make_response, redirect
import requests
import cgi, os
import json
import jwt
import cgitb; cgitb.enable()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

AUTHENTICATION_MANAGER = 'http://127.0.0.1:5001'
MODEL_APP_REPO = 'http://127.0.0.1:5002'
DEPLOYER = "http://127.0.0.1:5005"
SCHEDULER = "http://127.0.0.1:5010"
SCHBACK = "http://127.0.0.1:5011"

AUTH_URL = AUTHENTICATION_MANAGER + '/authenticate_user/'
CREATE_URL = AUTHENTICATION_MANAGER + '/create_user/'


@app.route('/')
def home():
   return render_template('index.html')

@app.route('/signin', methods = ['POST'])
def signin_page():
    user_type = request.form['user_type']
    return render_template('signin_page.html',user_type =  user_type, authcode="None",mesg="")

def session_expired(user_type,msg):
    message = "Session Expired! Please Login Again."
    if msg != "":
        message = msg 
    response = make_response(render_template('signin_page.html', user_type =  user_type, authcode="error_login", mesg = message))
    response.set_cookie('auth_token', "")
    return response

@app.route('/Dashboard/<user_type>', methods = ['GET','POST'])
def dashboard(user_type, auth_token ="" ):
  
    if auth_token == "":
        auth_token = request.cookies.get('auth_token')
        if auth_token == None:
            auth_token = request.headers.get('Authorization')
 
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'),algorithms=['HS256'])
    except:
        return session_expired(user_type,'')
    
    to_send={}
    #to_send["auth_token"] = auth_token
    to_send["username"] = payload['sub']

    # response = requests.post(MODEL_APP_REPO + '/get_models',json=to_send).content.decode()
    # model_list = response.split()
    
    response = make_response(render_template("dashboard.html",user_type=user_type,DEPLOYER = DEPLOYER))
    # if user_type == "Data_Scientist":
    #     response = make_response(render_template("data_sci_dashboard.html",response = model_list))
    #     response = make_response(render_template("data_sci_dashboard.html"))
    # elif user_type == "App_Developer":
    #     app_list = requests.post(MODEL_APP_REPO + '/get_all_models',json=to_send).content.decode().split()
    #     response = make_response(render_template("app_dev_dashboard.html",response = response, response2 = app_list , username=payload['sub']))

    response.set_cookie('auth_token', auth_token)
    return response 
    #return requests.post(SCHEDULER_ADDRESS,headers={'Authorization': session["auth_token"]},json={'username':username,'role':role})


@app.route('/register/<user_type>', methods = ['POST'])
def register(user_type):
    username=request.form['username']
    password=request.form['password']
    response = requests.post(CREATE_URL+user_type,json={'username':username,'password':password}).content.decode()
    payload = json.loads(response)
    if(payload["message"]=="Success"):
        return dashboard(user_type, payload['auth_token']);    
    else:
        return render_template('signin_page.html', user_type =  user_type, authcode="error_signup", mesg = payload["message"])


@app.route('/login/<user_type>', methods = ['POST'])
def login(user_type):
    username=request.form['username']
    password=request.form['password']
    response = requests.post(AUTH_URL+user_type,json={'username':username,'password':password}).content.decode()
    payload = json.loads(response)
    if(payload["message"]=="Success"):
        return dashboard(user_type, payload['auth_token']);    
    else:
        return render_template('signin_page.html', user_type =  user_type, authcode="error_login", mesg = payload["message"])


@app.route('/Upload/<user_type>', methods = ['POST'])
def upload(user_type):
    auth_token = request.cookies.get('auth_token')
    # user_type = ""
    # if type == "App":
    #     user_type = 'App_Developer' 
    # else:
    #     user_type = 'Data_Scientist' 
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'),algorithms=['HS256'])
        username = payload['sub']
        #f = request.files['filename']
        file_label = ['f1','f2','f3','f4','f5','f6']
        f=[]
        f.append(request.files['f1'])
        f.append(request.files['f2'])
        f.append(request.files['f3'])
        f.append(request.files['f4'])
        f.append(request.files['f5'])
        f.append(request.files['f6'])
        files = []
        for file,label in zip(f,file_label):
            files.append((label, (file.filename, file.read(), file.content_type)))
        
        to_send={}
        to_send["username"]=username
        to_send["role"]=user_type
        response=requests.post(DEPLOYER+'/submit',json=to_send,files=files).content.decode()
        # if user_type == 'App_Developer':
        #     to_send["app_name"]=f.filename
        #     f.save(os.path.join("./Data/Model/", f.filename))
        #     response=requests.post(MODEL_APP_REPO+'/add_app',json=to_send).content.decode()
        # else:
        #     to_send["model_name"]=f.filename
        #     f.save(os.path.join("./Data/App/", f.filename))
        #     response=requests.post(MODEL_APP_REPO+'/add_model',json=to_send).content.decode()
        if response == "ok":
            return render_template("temp.html",username=username,user_type=user_type,token=auth_token,URL=SCHBACK)
        else:
            return "error"
    except Exception as e:
        return session_expired(user_type,str(e))



if(__name__ == '__main__'):
    app.run(host ='127.0.0.1',port=5000,debug=True)
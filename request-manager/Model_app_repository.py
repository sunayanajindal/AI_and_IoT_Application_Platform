from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager, login_user, logout_user, login_required, UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Mod.db'
app.config['SECRET_KEY'] = 'secretkey'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class Models(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    model_name=db.Column(db.String(80), nullable=False)

class Apps(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    App_name=db.Column(db.String(80), nullable=False)



@app.route('/add_model', methods = ['GET', 'POST'])
def add_model():
    if(request.method=='POST'):
        data=request.get_json()
        username = data['username']
        model_name = data['model_name']

        # new_model = Models(username=username, model_name=model_name)
        # db.session.add(new_model)
        # db.session.commit()

        print("--------------------------=============================")
        check_model=Models.query.filter_by(model_name=model_name).first()
        if(check_model is None):
            new_model = Models(username=username, model_name=model_name)
            db.session.add(new_model)
            db.session.commit()
            print("-----------22---------=============================")
            return "ok"
        else:
            print("--------------22------------=============================")
            return "Model Already Present"
       

        # if(check_user is not None):
        #     return "User already registered, please sign in"
        # else:
        #     user = User_DS(username=username, password=password)
        #     db.session.add(user)
        #     db.session.commit()
        #     return "Registered Successfully"


@app.route('/add_app', methods = ['GET', 'POST'])
def add_app():
    if(request.method=='POST'):
        data=request.get_json()
        username = data['username']
        app_name = data['app_name']

        
        check_app=Apps.query.filter_by(App_name=app_name).first()
        if(check_app is None):
            new_app = Apps(username=username, App_name=app_name)
            db.session.add(new_app)
            db.session.commit()
            return "ok"
        else:
            return "App Already Present"
      




@app.route('/get_models', methods = ['GET', 'POST'])
def get_model():
    if(request.method=='POST'):
        print("hi")
        data=request.get_json()
        username = data['username']
        
        models = Models.query.filter_by(username=username).all()

        res=""

        for model in models:
            res+=model.model_name+" "

        if(res==""):
            return "NONE"
        return res

@app.route('/get_all_models', methods = ['GET', 'POST'])
def get_all_model():
    if(request.method=='POST'):
        print("hi")
        data=request.get_json()
        
        
        models = Models.query.all()

        res=""

        for model in models:
            res+=model.model_name+" "

        if(res==""):
            return "NONE"
        return res

@app.route('/get_apps', methods = ['GET', 'POST'])
def get_app():
    if(request.method=='POST'):
        data=request.get_json()
        username = data['username']
        
        apps = Apps.query.filter_by(username=username).all()

        res=""

        for app in apps:
            res+=app.App_name+" "

        if(res==""):
            return "NONE"
        return res


if(__name__ == '__main__'):
    db.create_all()
    app.run(port=1237,debug=True)
    

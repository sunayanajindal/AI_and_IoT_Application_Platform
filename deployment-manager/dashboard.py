from flask import Flask, request, redirect
from flask import render_template
import requests

app = Flask(__name__)

data = {}
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('dashboard.html', authcode=None)

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if (request.method == 'POST'):
        f1 = request.files["f1"]
        f2 = request.files["f2"]
        f3 = request.files["f3"]
        data['f1'] = f1.filename
        data['f2'] = f2.filename
        data['f3'] = f3.filename
        f4 = request.files["f4"]
        f5 = request.files["f5"]
        f6 = request.files["f6"]
        data['f4'] = f4.filename
        data['f5'] = f5.filename
        data['f6'] = f6.filename
        
        print(request.form.get('role'))
    
    print(data)
    r = requests.post('http://127.0.0.1:5000/',json=data)
    upload_file()    
    return render_template('dashboard.html', authcode=None)

def upload_file():
    uploaded_file1 = request.files['f1']
    uploaded_file2 = request.files['f2']
    uploaded_file3 = request.files['f3']
    uploaded_file4 = request.files['f4']
    uploaded_file5 = request.files['f5']
    uploaded_file6 = request.files['f6']
    if uploaded_file1.filename != '':
        uploaded_file1.save(uploaded_file1.filename)
    if uploaded_file2.filename != '':
        uploaded_file2.save(uploaded_file2.filename)
    if uploaded_file3.filename != '':
        uploaded_file3.save(uploaded_file3.filename)
    if uploaded_file4.filename != '':
        uploaded_file4.save(uploaded_file4.filename)
    if uploaded_file5.filename != '':
        uploaded_file5.save(uploaded_file5.filename)
    if uploaded_file6.filename != '':
        uploaded_file6.save(uploaded_file6.filename)
	
app.run(debug=True)
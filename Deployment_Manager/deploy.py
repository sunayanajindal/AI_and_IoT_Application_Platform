from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def deploy():
    r = request.get_json()
    print(r)
    
if __name__=="__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)

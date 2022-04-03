from encodings import utf_8
from Contract import Contract
import sys


str = ""

str += """import pickle
import json

from flask import Flask,request

app = Flask(__name__)\n\n"""

# contract_file = open('Contract.py','r')
print(sys.argv[1])
contract_file = open(sys.argv[1],'r')
print(type(contract_file),contract_file)
contract_as_string = contract_file.read()
contract_file.close()

str += contract_as_string

str += "\n\n"

str += """@app.route('/predict',methods=['POST'])
def predict():

    data = request.json
    # data is input data for pickel

    contract = Contract()

    preProcessedData = contract.preprocess(data)

    modelfile = open("""+sys.argv[2]+""",'rb')
    model = pickle.load(modelfile)

    prediction = model.predict(preProcessedData)

    return str(contract.postprocess(prediction))

if __name__ == '__main__':
    app.run()"""

wrapper_class = open('WrapperClass.py','w')
wrapper_class.write(str)
wrapper_class.close()


import pickle
import json

from flask import Flask,request

app = Flask(__name__)

class Contract:
    def preprocess(self,data):
        import numpy as np
        temp = []
        for key in data.keys():
            temp.append(data[key])
        data = np.array(temp).reshape((1, 5))
        return data

    def postprocess(self,data):
        s = "postprocessing... done"
        print(s)
        return data


@app.route('/predict',methods=['POST'])
def predict():

    data = request.json
    # data is input data for pickel

    contract = Contract()

    preProcessedData = contract.preprocess(data)

    modelfile = open('model.pkl','rb')
    model = pickle.load(modelfile)

    prediction = model.predict(preProcessedData)

    return str(contract.postprocess(prediction))

if __name__ == '__main__':
    app.run()
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

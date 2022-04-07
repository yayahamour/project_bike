from fastapi import FastAPI 
import uvicorn 
import pickle 
from models import Data
import numpy as np 
import json 
import pandas as pd 


def load_model(model): 
    savedmodel = open('./model/'+ model +'.pkl', 'rb')
    model = pickle.load(savedmodel)
    savedmodel.close()
    return model

app = FastAPI()

def read_predict(model, dico):
    dico = dico.dict()['data']
    pred = {}
    for key in dico['0'].keys():
        pred[key] = []
    for line in range(0,len(dico)):
        data = dico[str(line)]
        for key in data.keys():
            temp = pred[key]
            temp.append(data[key])
            pred[key] = temp
    df = pd.DataFrame(pred, index=np.arange(0,len(dico)))

    result = model.predict(df)
    response = []
    for i in result:
        response.append(int(i))
    return response


@app.post("/predict/{name}")
def prediction_lgbm( name, dico : Data):

    model = load_model(name)
    return json.dumps(read_predict(model, dico))


@app.get("/")
def pred():
    return {'Bonjour' : "Bonjour"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")


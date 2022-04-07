import urllib.request
import json
import os
import ssl

def convert_azure(df):
    tab = []
    col = {"Column2" : ""}
    for i, row in df.iterrows():
        tab.append({col ,row.to_dict()})
    return({"Inputs" : {"data" : tab}, "GlobalParameters" : 0.0})
  
def api_azure(data):
    data = convert_azure(data)
    body = str.encode(json.dumps(data))

    url = 'http://871c041d-2e05-4f25-9aa3-f5b57f00516f.westeurope.azurecontainer.io/score'
    api_key = '' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        return(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
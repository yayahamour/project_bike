import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here 
data = {
  "Inputs": {
    "data": [
      {
        "Column2": "example_value",
        "datetime": "2000-01-01T00:00:00.000Z",
        "season": 0,
        "holiday": 0,
        "workingday": 0,
        "weather": 0,
        "temp": 0.0,
        "atemp": 0.0,
        "humidity": 0,
        "windspeed": 0.0
      },
      {
        "Column2": "onsenfou",
        "datetime": "2000-01-01T00:00:00.000Z",
        "season": 2,
        "holiday": 1,
        "workingday": 0,
        "weather": 0,
        "temp": 20,
        "atemp": 21,
        "humidity": 15,
        "windspeed": 0.0
      }
    ]
  },
  "GlobalParameters": 0.0
}

body = str.encode(json.dumps(data))

url = 'https://modelvoting.westeurope.inference.ml.azure.com/score'
api_key = 'v3cMOaSe9XWkTnvbuThbWaSuvwPkEWPZ' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))

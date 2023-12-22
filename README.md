# TARA Machine Learning Model API

TARA API for Machine Learning Model built by CC Team using Flask. The API is used to retrieve a list of tourist attractions recommendations  

Be sure to install all the required modules before using the API:  
```
pip install -r requirements.txt
```

The API consists of only one endpoint: ```/get_recommendations``` 

You can try the API by using the URL:
```
https://tara-ml-72oh4bxmxq-as.a.run.app/get_recommendations
```  
accepting array of strings data as json.  

Send ```HTTP GET``` request with following request body format:  
```json
{
  "userPreferences": [
    "preference_1",
    "preference_2",
    "preference_n",
  ]
}
```

Each ```preference``` can be anything related to tourism (places, types, etc).

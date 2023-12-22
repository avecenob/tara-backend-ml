# TARA Machine Learning Model API

TARA API for Machine Learning Model built by CC Team using Flask. The API is used to retrieve a list of tourist attractions recommendations  

Be sure to install all the required modules before using the API:  
```pip install -r requirements.txt```

The API consists of only one endpoint:  
```https://tara-ml-72oh4bxmxq-as.a.run.app/get_recommendations```  
Send ```HTTP GET``` request with following request body:  
```{userPreferences: [array_of_strings]}```




How to install the app:
```  
python3 -m venv venv
. venv/bin/activate

pip install Flask
pip install Flask-API
pip install pytest
```  

[more details on how to install flask](https://flask.palletsprojects.com/en/1.1.x/installation/#installation)

Setup:
```    
export FLASK_APP=app
export FLASK_ENV=development
```

Initialise the DB with hardcoded data:
``` 
flask init-db
```   
Run:
``` 
flask run
``` 

Run tests:
```  
python -m pytest
```  
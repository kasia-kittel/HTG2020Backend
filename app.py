from flask import request, url_for
from flask_api import FlaskAPI

app = FlaskAPI(__name__)

@app.route('/healthcheck')
def healthcheck():
    return {'status': 'ok'}



if __name__ == "__main__":
    app.run(debug=True)
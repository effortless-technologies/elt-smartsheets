from flask import Flask
import smartsheet

app = Flask(__name__)
SMARTSHEET_ACCESS_TOKEN = "token"


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

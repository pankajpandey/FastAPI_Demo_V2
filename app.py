from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Docker..Pankaj is awesome and rich.. Dharam is super duper rich4'

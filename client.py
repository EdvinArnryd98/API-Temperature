import re

import requests as requests
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def get_data():
    data = requests.get('http://localhost:9080/get/').content
    result = data.decode('utf-8', 'ignore')
    text = result + ""
    line = re.sub('[\\\{}/"]', '', text)
    return render_template('index.html', temp=line), 200

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
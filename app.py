from flask import Flask, render_template, request, session
from mnums import MBRParser, MBRTransformer
import os


app = Flask(__name__)
app.secret_key = os.urandom(16)
parser = MBRParser('abc', MBRTransformer())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/input', methods=['POST'])
def parse_input():
    sent = request.data.decode('utf-8')
    result = parser.parse(sent)
    return {"result": result}

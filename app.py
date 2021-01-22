from flask import Flask, render_template, request, session
from mnums import MBRParser, MBRTransformer
import os


app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route('/')
def index():
    session['alphabet'] = 'abc'
    #session['parser'] = MBRParser('abc', MBRTransformer()).__dict__
    return render_template('index.html')

@app.route('/input', methods=['POST'])
def parse_input():
    alphabet = session['alphabet']
    parser = MBRParser(alphabet, MBRTransformer())
    sent = request.data.decode('utf-8')
    try:
        result = parser.parse(sent)
        return {"result": result}
    except:
        return {"result": "There was an error. Please check your expression."}, 400

@app.route('/alphabet', methods=['POST'])
def change_alphabet():
    try:
        alpha = request.json['first-letter']
        omega = request.json['last-letter']
        alphabet = "".join(map(chr, range(ord(alpha), ord(omega)+1)))
        print(alphabet)
        session['alphabet'] = alphabet
        return ('', 200)
    except:
        return ('', 400)

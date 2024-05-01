from flask import Flask, jsonify, render_template, request
from ipynb.fs.full.sol import *

from sol import get_responce

app = Flask(__name__,  template_folder='../static')



def get_res(prompt):
    response = get_responce(prompt)
    print(response)
    return response.text


@app.route("/")
def home():    
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def get_bot_response():   
    data = request.get_json()
    print(data)
    text = data.get('prompt') 
    user_input = text
    output = get_res(user_input)
    return jsonify({"response":True,"message":output})


if __name__ == "__main__":
    app.run()




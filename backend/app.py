from flask import Flask, request, jsonify
from utils import lookup_ein, get_response
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)




# Your existing functions here (lookup_ein, create_prompt, get_completion, etc.)

@app.route('/')
def index():
    return "Welcome to the Charity Data Lookup Service!"


@app.route('/lookup', methods=['POST'])
def lookup_charity():
    # get the EIN from the request body
    ein = request.json.get('ein', None)

    # validate the EIN
    if not ein:
        return jsonify({'error': 'EIN is required'}), 400

    charity_info = lookup_ein(ein)  
    if 'error' in charity_info:
        return jsonify(charity_info), 404

    ai_response = get_response(charity_info)
    return jsonify(ai_response)

# a route to get data of the charity
@app.route('/data/<ein>', methods=['GET'])
def get_data(ein):
    charity_info = lookup_ein(ein)
    print(charity_info)
    if not ein:
        return jsonify({'error': 'EIN is required'}), 400

    charity_info = lookup_ein(ein)  
    if 'error' in charity_info:
        return jsonify(charity_info), 404

    return jsonify(charity_info)


if __name__ == '__main__':
    app.run(debug=True)

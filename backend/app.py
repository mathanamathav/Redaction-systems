# app.py
from flask import Flask, request, jsonify
import requests

API_ENDPOINT = "http://127.0.0.1:8500/ner_text_labelling"

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# todo simple text api input
@app.route('/process_text', methods=['POST'])
def process_text():
    input_data = request.json.get("text_input" , "")

    if input_data:

        response = requests.post(
                API_ENDPOINT, json={"text": input_data})
        
        if response.status_code == 200:
            result_text = response.json()
            # todo Do the machine learning part and set the values

            modified_text = result_text.get("text" , "")        
            mappings = result_text.get("labelling" , "")

            response_data = {
                'data': modified_text,
                'mappings': mappings
            }
            return jsonify(response_data), 200
    else:
        return jsonify({'error': 'Invalid input format'}), 400


# todo batch text inputs

if __name__ == '__main__':
    app.run(port=8000 , debug=True)

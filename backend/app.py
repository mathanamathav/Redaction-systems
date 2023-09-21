# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

# todo simple text api input


@app.route('/process_text', methods=['POST'])
def process_text():
    input_data = request.json

    if 'text_input' in input_data:
        text_input = input_data['text_input']

        # todo Do the machine learning part and set the values
        modified_text = "asdasd"        
        mappings = { "asdas" : "asdasdsa"}

        response_data = {
            'data': modified_text,
            'mappings': mappings
        }
        return jsonify(response_data), 200
    else:
        return jsonify({'error': 'Invalid input format'}), 400


# todo batch text inputs

if __name__ == '__main__':
    app.run(debug=True)

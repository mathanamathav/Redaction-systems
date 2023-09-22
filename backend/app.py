# app.py
from flask import Flask, request, jsonify
from utils import redaction_code,ner_text_labelling
import threading
import queue

import requests

app = Flask(__name__)

response_queue  = queue.Queue()

def process_request(request_data):
    response = ner_text_labelling({"text": request_data})

    text = response.get("text", "")
    labels = response.get("labelling", "")

    modified_text, mappings = redaction_code(text, labels)
    response = {"data": modified_text, "mappings": mappings}
    response_queue.put(response)


@app.route("/")
def hello_world():
    return "Hello, World!"


# todo simple text api input
@app.route("/process_text", methods=["POST"])
def process_text():
    input_data = request.json.get("text_input", "")

    if input_data:
        response = ner_text_labelling({"text": input_data})

        text = response.get("text", "")
        labels = response.get("labelling", "")

        modified_text, mappings = redaction_code(text, labels)
        response_data = {"data": modified_text, "mappings": mappings}

        return jsonify(response_data), 200
    else:
        return jsonify({"error": "Invalid input format"}), 400


# todo batch text inputs
@app.route("/batch_text", methods=["POST"])
def batch_text():
    input_data = request.json.get("text_input", "")
    if not input_data:
        return jsonify({"error": "Invalid input format"}), 400
    
    threads = []
    for request_data in input_data:
        thread = threading.Thread(target=process_request, args=(request_data,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    responses = []
    while not response_queue.empty():
        response = response_queue.get()
        responses.append(response)

    return jsonify({'responses': responses})



if __name__ == "__main__":
    app.run(port=8000, debug=True)

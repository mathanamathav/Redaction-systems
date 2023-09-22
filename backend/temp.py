# app.py
from flask import Flask, request, jsonify
from utils import redaction_code,ner_text_labelling
import threading
import queue
import time
import requests

app = Flask(__name__)



# Create a queue to hold incoming bulk requests
response_queue  = queue.Queue()
input_queue = queue.Queue()

# Function to simulate processing for each request
def thread_func(id):
    while True:
        if input_queue.empty():
            time.sleep(2/id)
        else:
            response_queue.put(process_request(input_queue))


thread_num = 8
threads = []
for id in range(thread_num):
    thread = threading.Thread(target=thread_func, args=(id,))
    thread.start()
    threads.append(thread)

def response_handler():
    responses = {}
    while True: 
        if not response_queue.empty():
            response = response_queue.get()
            if (response["id"],response["origin"]) in responses.keys:
                responses[(response["id"],response["origin"])].append(response["data"])
            else:
                responses[(response["id"],response["origin"])]=[response["data"]]
            for id,origin in responses.keys():
                pass

# Function to simulate processing for each request
def process_request(request_data):
    response = ner_text_labelling({"text": request_data})

    text = response.get("text", "")
    labels = response.get("labelling", "")

    modified_text, mappings = redaction_code(text, labels)
    response = {"data": modified_text, "mappings": mappings}
    response_queue.put(response)
    return response


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
    

    for request_data in input_data:
        input_queue.put(request_data)

    # Collect responses from the queue
    


    return jsonify({'responses': responses})




if __name__ == "__main__":
    app.run(port=8000, debug=True)

# app.py
from flask import Flask, request, jsonify
from utils import redaction_code, ner_text_labelling
import threading
import queue

app = Flask(__name__)

response_queue = queue.Queue()


def process_request(request_data):
    response = ner_text_labelling({"text": request_data})

    text = response.get("text", "")
    labels = response.get("labelling", "")

    modified_text, mappings, modified_text_read, mappings_read = redaction_code(
        text, labels
    )

    response = {
        "data": modified_text,
        "mappings": mappings,
        "read_data": modified_text_read,
        "read_mappings": mappings_read,
    }
    response_queue.put(response)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/process_text", methods=["POST"])
def process_text():
    input_data = request.json.get("text_input", "")

    if input_data:
        response = ner_text_labelling({"text": input_data})

        text = response.get("text", "")
        labels = response.get("labelling", "")

        modified_text, mappings, modified_text_read, mappings_read = redaction_code(
            text, labels
        )
        response_data = {
            "data": modified_text,
            "mappings": mappings,
            "read_data": modified_text_read,
            "read_mappings": mappings_read,
        }

        return jsonify(response_data), 200
    else:
        return jsonify({"error": "Invalid input format"}), 400


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

    modified_text, mappings, modified_text_read, mappings_read = [], [], [], []
    while not response_queue.empty():
        response = response_queue.get()

        modified_text.append(response.get("data"))
        mappings.append(response.get("mappings"))
        modified_text_read.append(response.get("read_data"))
        mappings_read.append(response.get("read_mappings"))

    return jsonify(
        {
            "data": modified_text,
            "mappings": mappings,
            "read_data": modified_text_read,
            "read_mappings": mappings_read,
        }
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True)

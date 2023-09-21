# app.py
from flask import Flask, request, jsonify
import spacy
import json
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_lg"}],
}
provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine = provider.create_engine()
analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["en"])

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! NER Server'


@app.route("/ner_text_labelling", methods=["POST"])
def ner_text_labelling():
    input_data = request.json.get("text" , "")
    if input_data:
        results = analyzer.analyze(text=input_data,
                                   language='en')
        response_data = {
            "text": input_data,
            "labelling": [data.to_dict() for data in results]
        }
        return jsonify(response_data), 200
    else:
        return jsonify({'error': 'Invalid input format'}), 400


if __name__ == '__main__':
    app.run(port=8500, debug=True)

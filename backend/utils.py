from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_lg"}],
}

provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine = provider.create_engine()
analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["en"])


def ner_text_labelling(data):
    input_data = data.get("text" , "")
    results = analyzer.analyze(text=input_data,
                                language='en')
    resp_data = {
        "text": input_data,
        "labelling": [data.to_dict() for data in results]
    }
    return resp_data

def redaction_code(sentence, entities_info):
    count_map = {}

    for val in entities_info:
        count_map[val["entity_type"]] = 1 + count_map.get(val["entity_type"], 0)

    temp_dic = {}

    for entity_info in entities_info:
        entity_type = entity_info["entity_type"]
        start_index = entity_info["start"]
        end_index = entity_info["end"]

        entity = sentence[start_index: end_index]

        if entity in temp_dic:
            continue
        else:
            temp_dic[entity] = entity_type

    for val in count_map:
        if count_map[val] > 1:
            count = 1
            for key, ent in temp_dic.items():
                if val == ent:
                    temp_dic[key] = val + str(count)
                    count += 1

    for vals in temp_dic:
        sentence = sentence.replace(vals, temp_dic[vals])

    return sentence , temp_dic

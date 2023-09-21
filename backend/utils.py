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

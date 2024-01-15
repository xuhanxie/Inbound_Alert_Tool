def json_parse(json_data, key_to_find):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == key_to_find:
                return value
            elif isinstance(value, (dict, list)):
                result = json_parse(value, key_to_find)
                if result is not None:
                    return result

    elif isinstance(json_data, list):
        for item in json_data:
            if isinstance(item, (dict, list)):
                result = json_parse(item, key_to_find)
                if result is not None:
                    return result

    return None

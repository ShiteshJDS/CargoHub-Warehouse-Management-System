# api/validators.py
def validate_data(data, required_keys, key_types):
    missing_keys = [key for key in required_keys if key not in data]
    extra_keys = [key for key in data if key not in required_keys]
    empty_values = [key for key in data if data[key] == ""]
    wrong_types = [key for key in data if key in key_types and not isinstance(data[key], key_types[key])]

    if missing_keys or extra_keys or empty_values or wrong_types:
        return False, {
            "missing_keys": missing_keys,
            "extra_keys": extra_keys,
            "empty_values": empty_values,
            "wrong_types": wrong_types
        }
    return True, {}
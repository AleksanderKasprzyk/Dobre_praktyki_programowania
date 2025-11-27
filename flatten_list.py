# flatten_list.py

def flatten_list(nested_list):
    result = []

    def _flatten(item):
        if isinstance(item, list):
            for element in item:
                _flatten(element)
        else:
            result.append(item)

    _flatten(nested_list)
    return result

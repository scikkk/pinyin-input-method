import json


def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as fr:
        return json.load(fr)


def save_json(obj, filename):
    """
    @function: write data into json files
    @filename: json filename
    @data: the probability matrix
    """
    with open(filename, mode='w', encoding='utf-8') as fw:
        data = json.dumps(obj, indent=4, sort_keys=True, ensure_ascii=False)
        fw.write(data)

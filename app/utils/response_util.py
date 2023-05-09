import json


def response_msg(content: str, msg: str):
    response_object = {f"{content}": msg}
    json_content = json.dumps(response_object)
    return json_content

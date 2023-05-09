import json


def response_msg(content: str, msg: str):
    response_object = {f"{content}": msg}
    json_content = json.dumps(response_object)
    return json_content


def update_response(content: str, updated_user: dict):
    response_object = {f"{content}": updated_user}
    json_content = json.dumps(response_object)
    return json_content

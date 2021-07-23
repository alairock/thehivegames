import json


def encode_dict(dict_data):
  message = f"data: {json.dumps(dict_data)}"
  message += "\r\n\r\n"
  return message.encode("utf-8")

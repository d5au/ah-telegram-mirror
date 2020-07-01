import json

class VictimInfo:

    def __init__(self, author_id: int, message_content: str, message_text: str):
        self.author_id = author_id
        self.message_content = message_content
        self.message_text = message_text

    def to_json(self):
        return json.dumps({
            'author_id': self.author_id,
            'msg_content': self.message_content,
            'msg_text': self.message_text
        })

def victim_from_json(j: str):
    obj = json.loads(j)
    return VictimInfo(obj['author_id'], obj['msg_content'], obj['msg_text'])
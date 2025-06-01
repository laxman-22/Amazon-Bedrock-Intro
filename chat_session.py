class ChatSession:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({
            "role": role,
            "content": [{"type": "text", "text": content}]
        })

    def clear_session(self):
        self.message = []
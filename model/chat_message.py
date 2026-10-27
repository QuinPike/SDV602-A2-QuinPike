class ChatMessage:

    def __init__(self, username, text, timestamp=None):
        self.username = username
        self.text = text
        self.timestamp = timestamp
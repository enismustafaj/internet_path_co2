class TokenState:
    def __init__(self, tokens, token_index):
        self.tokens = tokens
        self.token_index = token_index

    def update_token_state(self):
        self.token_index += 1
        if self.token_index == len(self.tokens):
            self.token_index = 0

    def get_token_state(self):
        return self.tokens[self.token_index]

class TokenState:

    """
    This class is used to manage the state of the API tokens.
    """

    def __init__(self, tokens, token_index):
        self.tokens = tokens
        self.token_index = token_index

    # Update the token state
    def update_token_state(self):
        self.token_index += 1
        if self.token_index == len(self.tokens):
            self.token_index = 0

    # Get the current token
    def get_token_state(self):
        return self.tokens[self.token_index]

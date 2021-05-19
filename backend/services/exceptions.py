class JWTException(Exception):
    """Causes when some error is occurred during JWT validation/obtaining."""
    def __init__(self, payload, **kwargs):
        self.kwargs = kwargs
        self.message = self.get_message(payload)
        super(JWTException, self).__init__(self.message)

    @staticmethod
    def get_message(payload):
        return f'Token error. Payload: {payload}.'

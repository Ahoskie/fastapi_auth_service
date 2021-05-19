class DatabaseException(Exception):
    """Causes when some suspicious operation is being applied to database."""
    def __init__(self, payload, **kwargs):
        self.kwargs = kwargs
        self.message = self.get_message(payload)
        # logger.error(self.message) IMPLEMENT LOGGING LATER!
        super(DatabaseException, self).__init__(self.message)

    @staticmethod
    def get_message(payload):
        return f'Database operation error occurred. Payload: {payload}.'


class NotFoundException(DatabaseException):
    @staticmethod
    def get_message(payload):
        return f'Not found. Payload: {payload}.'

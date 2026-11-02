class ApiError(Exception):
    """Base exception for errors that map to a JSON HTTP response."""

    status_code = 400
    error = "Bad Request"

    def __init__(self, message, error=None, status_code=None):
        super().__init__(message)
        self.message = message
        if error is not None:
            self.error = error
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {"error": self.error, "message": self.message}

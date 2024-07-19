class ServiceError(Exception):

    def __init__(self, message=None, error_code=None):
        super().__init__(message)
        self.message = message or "A service error occurred."
        self.error_code = error_code or 500

    def to_dict(self):
        return {"error": self.message, "code": self.error_code}


class DatabaseError(ServiceError):

    def __init__(self, message=None, error_code=500):
        super().__init__(message or "A database error occurred.", error_code)


class ValidationError(ServiceError):

    def __init__(self, message=None, error_code=400):
        super().__init__(message or "A validation error occurred.", error_code)


class NotFoundError(ServiceError):

    def __init__(self, message=None, error_code=404):
        super().__init__(message or "The requested resource was not found.", error_code)


class UnauthorizedError(ServiceError):

    def __init__(self, message=None, error_code=401):
        super().__init__(message or "Unauthorized access.", error_code)

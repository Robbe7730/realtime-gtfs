"""
exceptions.py: contains realtime_gtfs Exceptions
"""

class InvalidKeyError(RuntimeError):
    """
    InvalidKeyError: raised when an invalid key is being set
    """
    def __init__(self, arg):
        self.args = ["Invalid key " + arg]
        RuntimeError.__init__(self)

class InvalidValueError(RuntimeError):
    """
    InvalidValueError: raised when an invalid value is being used
    """
    def __init__(self, arg):
        self.args = ["Invalid value for key " + arg]
        RuntimeError.__init__(self)

class MissingKeyError(RuntimeError):
    """
    MissingKeyError: raised when a required key is not set
    """
    def __init__(self, arg):
        self.args = ["Missing key " + arg]
        RuntimeError.__init__(self)

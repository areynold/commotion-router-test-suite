"""Custom exceptions for the Commotion Router Test Suite"""

import requests

class CommotionIPError(ConnectionError):
    """
    Raised when the test host does not have a valid Commotion IP address.
    Subclass of the built-in ConnectionError base class.
    """

    def __init__(self, arg):
        self.msg = (
            "No valid Commotion IP address found on any network interface"
            )
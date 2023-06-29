class InvalidArgumentError(Exception):
    """Error raised for invalid arguments"""


class MissingArgumentError(Exception):
    """Error raised for missing arguments"""


class ResponseFormattingError(Exception):
    """Error raised when formatting API response"""


class InvalidSerializedRestliError(Exception):
    """Error raised when an incorrectly serialized Rest.li string is encountered"""

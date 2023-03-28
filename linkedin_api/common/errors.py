class InvalidArgumentError(Exception):
    "Error raised for invalid arguments"
    pass


class MissingArgumentError(Exception):
    "Error raised for missing arguments"
    pass


class ResponseFormattingError(Exception):
    "Error raised when formatting API response"
    pass

class InvalidSerializedRestliError(Exception):
    "Error raised when an incorrectly serialized Rest.li string is encountered"
    pass
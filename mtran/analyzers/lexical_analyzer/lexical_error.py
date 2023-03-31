from enum import Enum

class ErrorTypes(Enum):

    ERROR_CLASSIFICATION = "Lexical Error: "
    STANDARD_ERROR = "Invalid character"
    UNCLOSED_QUOTE = "Unclosed quote"
    EXTRA_DOT = "Extra dot"
    UNCLOSED_CURLY_BRACE = "Unclosed curly brace"


class LexicalError(Exception):

    def __init__(self, line_num, column_num,
                 message=ErrorTypes.STANDARD_ERROR.value):
        self.line_num = line_num
        self.column_num = column_num
        self.message = ErrorTypes.ERROR_CLASSIFICATION.value + \
            f"{message}:{self.line_num}:{self.column_num}"
        super().__init__(self.message)

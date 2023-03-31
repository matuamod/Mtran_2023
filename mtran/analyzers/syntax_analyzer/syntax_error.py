from enum import Enum

class ErrorTypes(Enum):
    
    ERROR_CLASSIFICATION = "Syntax Error: "
    STANDART_ERROR = "Invalid syntax"
    TYPE_ERROR = "Type error"
    ASSIGNMENT_ERRROR = "Assignment error"
    IDENTIFIER_ERROR = "Identifier error"
    CONSTANT_ERROR = "Constant error"
    SEMICOLON_ERROR = "Semicolon error"


class SyntaxError(Exception):
    
    def __init__(self, line_num, column_num,
                 message=ErrorTypes.STANDART_ERROR.value):
        self.line_num=line_num,
        self.column_num=column_num,
        self.message=ErrorTypes.ERROR_CLASSIFICATION.value + \
            f"{message}:{self.line_num[0]}:{self.column_num[0]}"
        super().__init__(self.message)
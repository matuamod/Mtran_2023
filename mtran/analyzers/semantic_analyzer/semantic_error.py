from enum import Enum

class ErrorTypes(Enum):
    
    ERROR_CLASSIFICATION = "Semantic Error: "
    STANDART_ERROR = "Invalid for semantic rules"
    DUBLICATE_ERROR = "Dublicate error"
    SYMBOL_ERROR = "Symbol error"
    COMPARISON_ERROR = "Comparison operation error"
    ASSIGNMENT_ERRROR = "Assignment operation error"
    BINARY_OP_ERROR = "Binary operation error"
    LOGICAL_OP_ERROR = "Logical operation error"
    IDENTIFIER_ERROR = "Identifier error"


class SemanticError(Exception):
    
    def __init__(self, addition, message=ErrorTypes.STANDART_ERROR.value):
        self.message=ErrorTypes.ERROR_CLASSIFICATION.value + f"{message}. {addition}"
        super().__init__(self.message)
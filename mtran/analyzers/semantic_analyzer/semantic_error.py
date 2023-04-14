from enum import Enum

class ErrorTypes(Enum):
    
    ERROR_CLASSIFICATION = "Semantic Error: "
    STANDART_ERROR = "Invalid for semantic rules"
    DUBLICATE_ERROR = "Dublicate error"
    SYMBOL_ERROR = "Symbol error"
    INPUT_ERROR = "Readln argument error"
    IF_COMPARISON_ERROR = "If statement comparison type error"
    COMPARISON_ERROR = "Comparison operation error"
    ASSIGNMENT_ERRROR = "Assignment operation error"
    BINARY_OP_ERROR = "Binary operation error"
    LOGICAL_OP_ERROR = "Logical operation error"
    IDENTIFIER_ERROR = "Identifier error"
    FOR_LOOP_ERROR = "For loop execution condition error"
    WHILE_LOOP_ERROR = "While loop execution condition error"
    UNTIL_LOOP_ERROR = "Repeat..Until loop execution condition error"
    CASE_COMPOUND_ERROR = "Case compound condition error"


class SemanticError(Exception):
    
    def __init__(self, addition, message=ErrorTypes.STANDART_ERROR.value):
        self.message=ErrorTypes.ERROR_CLASSIFICATION.value + f"{message}. {addition}"
        super().__init__(self.message)
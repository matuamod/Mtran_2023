from enum import Enum

class TOKEN_TYPES(Enum):
    # - Reserved names
    PROGRAM = "PROGRAM" #

    PROCEDURE = "PROCEDURE" #

    BEGIN = "BEGIN" #

    ID = "ID"
    VAR = "VAR" #
    TYPE = "TYPE" #
    CONST = "CONST" #

    INTEGER = "INTEGER" #
    INTEGER_CONST = "INTEGER_CONST"
    REAL = "REAL" # 
    REAL_CONST = "REAL_CONST"
    CHAR = "CHAR" #
    CHAR_CONST = "CHAR_CONST"
    STRING = "STRING" #
    STRING_CONST = "STRING_CONST"
    BOOLEAN = "BOOLEAN" #
    BOOLEAN_CONST = "BOOLEAN_CONST"
    ARRAY = "ARRAY" #

    PLUS = "PLUS"
    PLUS_EQUAL = "PLUS_EQUAL"
    MINUS = "MINUS"
    MINUS_EQUAL = "MINUS_EQUAL"
    MUL = "MUL"
    MUL_EQUAL = "MUL_EQUAL"
    FLOAT_DIV = "FLOAT_DIV"
    DIV_EQUAL = "DIV_EQUAL"
    INTEGER_DIV = "DIV" #
    MOD = "MOD" #
    AND = "AND" #
    XOR = "XOR" #
    OR = "OR" #
    RPAREN = "RPAREN"
    LPAREN = "LPAREN"
    RCURLY_BRACE = "RCURLY_BRACE"
    LCURLY_BRACE = "LCURLY_BRACE"
    RSQUARE_BRACE = "RSQUARE_BRACE"
    LSQUARE_BRACE = "LSQUARE_BRACE" 
    EOF = "EOF"
    ASSINGMENT = "ASSINGMENT"
    SEMICOLON = "SEMICOLON"
    EQUAL = "EQUAL"
    NONEQUAL = "NONEQUAL"
    GREATER = "GREATER"
    LESS = "LESS"
    GREATER_OR_EQUAL = "GREATER_OR_EQUAL"
    LESS_OR_EQUAL = "LESS_OR_EQUAL"
    COMMA = "COMMA"
    COLON = "COLON"
    DOT = "DOT"

    WRITELN = "WRITELN" #
    WRITE = "WRITE" #
    READLN = "READLN" #

    IF = "IF" #
    ELSE = "ELSE" #
    THEN = "THEN" #

    FOR = "FOR" #
    WHILE = "WHILE" #
    REPEAT = "REPEAT" #
    TO = "TO" #
    DO = "DO" #
    UNTIL = "UNTIL" #

    CASE = "CASE" #
    OF = "OF" #

    END = "END" #


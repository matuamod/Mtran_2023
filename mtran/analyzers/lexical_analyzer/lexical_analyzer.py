from .lexical_error import LexicalError
from .lexical_error import ErrorTypes
from .tokens import Token
from .tokens import TOKEN_TYPES
from .tokens import RESERVED_TOKENS

class LexicalAnalyzer(object):

    def __init__(self, text):
        # Client input expression
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.line_num = 1
        self.column_num = 0
        # Current char
        self.current_char = self.text[self.pos]


    def error(self, message):
        raise LexicalError(self.line_num, self.column_num, message)


    def skip_comment(self):
        while self.current_char != "}" and self.current_char is not None:
            self.advance()

        if self.current_char == None:
            self.error(ErrorTypes.UNCLOSED_CURLY_BRACE.value)

        self.advance()


    def advance(self):
        self.pos += 1

        if self.pos > len(self.text) - 1:
            self.current_char = None
        else: 
            self.column_num += 1

            if self.current_char == "\n":
                self.line_num += 1
                self.column_num = 1

            self.current_char = self.text[self.pos]


    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()


    def parse_integer(self):
        result = str()

        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == ".":
            result += self.current_char
            self.advance()
            return self.parse_real(result)

        return Token(TOKEN_TYPES.INTEGER_CONST.value, int(result))


    def parse_real(self, part_number):
        while self.current_char is not None and self.current_char.isdigit():
            part_number += self.current_char
            self.advance()

        if self.current_char == ".":
            self.error(ErrorTypes.EXTRA_DOT.value)

        return Token(TOKEN_TYPES.REAL_CONST.value, float(part_number))


    def parse_string(self):
        result = str()

        while self.current_char is not None and self.current_char.isalnum() \
            or self.current_char is not None and self.current_char.isspace():
            result += self.current_char
            self.advance()

        if self.current_char != "'":
            self.error(ErrorTypes.UNCLOSED_QUOTE.value)

        self.advance()

        if len(result) == 1:
            return Token(TOKEN_TYPES.CHAR_CONST.value, result)
        else:
            return Token(TOKEN_TYPES.STRING_CONST.value, result) 


    def peek(self):
        next_pos = self.pos + 1

        if next_pos > len(self.text) - 1:
            return None
        else:
            return self.text[next_pos]


    def get_next_id_token(self):
        result = str()

        # Example: "abc123".isalnum() = True - For creating new Id Tokens for variables
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        if result.lower() in ("true", "false"):
            return Token(TOKEN_TYPES.BOOLEAN_CONST.value, result.upper())

        token = RESERVED_TOKENS.get(result, Token(TOKEN_TYPES.ID.value, result))
        return token


    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char == "{":
                self.skip_comment()
                continue
            elif self.current_char.isspace():
                self.skip_whitespace()
                continue
            # Example: "abc".isalpha() = True - For checking variables and keywords
            elif self.current_char.isalpha():
                return self.get_next_id_token()
            elif self.current_char.isdigit():
                return self.parse_integer()
            elif self.current_char == "'":
                self.advance()
                return self.parse_string()
            elif self.current_char == ":":

                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(TOKEN_TYPES.ASSINGMENT.value, ":=")

                self.advance()
                return Token(TOKEN_TYPES.COLON.value, ":")
            elif self.current_char == "<":

                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(TOKEN_TYPES.LESS_OR_EQUAL.value, "<=")
                elif self.peek() == ">":
                    self.advance()
                    self.advance()
                    return Token(TOKEN_TYPES.NONEQUAL.value, "<>")

                self.advance()
                return Token(TOKEN_TYPES.LESS.value, "<")
            elif self.current_char == ">":

                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(TOKEN_TYPES.GREATER_OR_EQUAL.value, ">=")

                self.advance()
                return Token(TOKEN_TYPES.GREATER.value, ">")
            elif self.current_char == "=":
                self.advance()
                return Token(TOKEN_TYPES.EQUAL.value, "=")
            elif self.current_char == "+":

                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(TOKEN_TYPES.PLUS_EQUAL.value, "+=")    

                self.advance()
                return Token(TOKEN_TYPES.PLUS.value, "+")
            elif self.current_char == "-":

                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(TOKEN_TYPES.MINUS_EQUAL.value, "-=")    

                self.advance()
                return Token(TOKEN_TYPES.MINUS.value, "-")
            elif self.current_char == "*":

                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(TOKEN_TYPES.MUL_EQUAL.value, "*=")    

                self.advance()
                return Token(TOKEN_TYPES.MUL.value, "*")
            elif self.current_char == "/":

                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(TOKEN_TYPES.DIV_EQUAL.value, "/=")    

                self.advance()
                return Token(TOKEN_TYPES.FLOAT_DIV.value, "/")
            elif self.current_char == ")":
                self.advance()
                return Token(TOKEN_TYPES.RPAREN.value, ")")
            elif self.current_char == "(":
                self.advance()
                return Token(TOKEN_TYPES.LPAREN.value, "(")
            elif self.current_char == "]":
                self.advance()
                return Token(TOKEN_TYPES.RSQUARE_BRACE.value, "]")
            elif self.current_char == "[":
                self.advance()
                return Token(TOKEN_TYPES.LSQUARE_BRACE.value, "[")
            elif self.current_char == ",":
                self.advance()
                return Token(TOKEN_TYPES.COMMA.value, ",")
            elif self.current_char == ";":
                self.advance()
                return Token(TOKEN_TYPES.SEMICOLON.value, ";")
            elif self.current_char == ".":
                self.advance()
                return Token(TOKEN_TYPES.DOT.value, ".")
            else:
                self.error(ErrorTypes.STANDARD_ERROR.value)

        return Token(TOKEN_TYPES.EOF.value, None)

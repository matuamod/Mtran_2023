from .AST import *
from ..lexical_analyzer import TOKEN_TYPES, ConfigureTables


class SyntaxAnalyzer(object):

    def __init__(self, lexical_analyzer):
        # lexical_analyzer initialization
        self.lexical_analyzer = lexical_analyzer
        # Current token instance
        self.current_token = self.lexical_analyzer.get_next_token()
        # Configure tables instance init
        self.conf = ConfigureTables()
        # Add current token to table  
        self.conf.fill_table(self.current_token)


    def error(self):
        raise Exception("Error. Invalid syntax")


    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexical_analyzer.get_next_token()
            self.conf.fill_table(self.current_token)
        else:
            self.error()


    def parse_paren(self):
        self.eat(TOKEN_TYPES.LPAREN.value)
        node = self.parse_expr()
        self.eat(TOKEN_TYPES.RPAREN.value)
        return node


    def parse_factor(self):
        token = self.current_token

        match token.type:
            case TOKEN_TYPES.PLUS.value:
                self.eat(TOKEN_TYPES.PLUS.value)
                return UnaryOperation(
                    token=token,
                    expr=self.parse_factor()
                )

            case TOKEN_TYPES.MINUS.value:
                self.eat(TOKEN_TYPES.MINUS.value)
                return UnaryOperation(
                    token=token,
                    expr=self.parse_factor()
                )
            
            case TOKEN_TYPES.INTEGER_CONST.value:
                self.eat(TOKEN_TYPES.INTEGER_CONST.value)
                return Number(token)
                
            case TOKEN_TYPES.LPAREN.value:
                return self.parse_paren()
            
            case _:
                return self.parse_variable()


    def parse_term(self):
        node = self.parse_factor()

        while self.current_token.type in (
                TOKEN_TYPES.MUL.value,
                TOKEN_TYPES.FLOAT_DIV.value,
                TOKEN_TYPES.INTEGER_DIV.value):

            token = self.current_token

            match self.current_token.type:
                case TOKEN_TYPES.MUL.value:
                    self.eat(TOKEN_TYPES.MUL.value)

                case TOKEN_TYPES.INTEGER_DIV.value:
                    self.eat(TOKEN_TYPES.INTEGER_DIV.value)

                case TOKEN_TYPES.FLOAT_DIV.value:
                    self.eat(TOKEN_TYPES.FLOAT_DIV.value)

            node = BinaryOperation(
                left_node=node,
                token=token,
                right_node=self.parse_factor()
            )

        return node


    def parse_expr(self):
        node = self.parse_term()

        while self.current_token.type in (
                TOKEN_TYPES.MINUS.value,
                TOKEN_TYPES.PLUS.value):

            token = self.current_token

            if self.current_token.type == TOKEN_TYPES.PLUS.value:
                self.eat(TOKEN_TYPES.PLUS.value)
            elif self.current_token.type == TOKEN_TYPES.MINUS.value:
                self.eat(TOKEN_TYPES.MINUS.value)

            node = BinaryOperation(
                left_node=node,
                token=token,
                right_node=self.parse_term()
            )

        return node


    def parse_program(self):
        node = self.parse_compound_statement()
        self.eat(TOKEN_TYPES.DOT.value)
        return node


    def parse_compound_statement(self):
        self.eat(TOKEN_TYPES.BEGIN.value)
        nodes_list = self.parse_statement_list()
        self.eat(TOKEN_TYPES.END.value)

        compound_statement = CompoundStatement()

        for node in nodes_list:
            compound_statement.statement_list.append(node)  

        return compound_statement 


    def parse_statement_list(self):
        statement_list = list()
        node = self.parse_statement()
        statement_list.append(node)

        while self.current_token.type == TOKEN_TYPES.SEMICOLON.value:
            self.eat(TOKEN_TYPES.SEMICOLON.value)
            statement_list.append(self.parse_statement())

        if self.current_token.type == TOKEN_TYPES.ID.value:
            self.error()

        return statement_list


    def parse_statement(self):
        match self.current_token.type:
            case TOKEN_TYPES.BEGIN.value:
                node = self.parse_compound_statement()

            case TOKEN_TYPES.ID.value:
                 node = self.parse_assignment_statement()
                 
            case _:
                node = self.parse_empty()

        return node


    def parse_assignment_statement(self):
        left_node = self.parse_variable()
        token = self.current_token
        self.eat(TOKEN_TYPES.ASSINGMENT.value)
        right_node = self.parse_expr()

        node = AssignmentStatement(left_node, token, right_node)
        return node


    def parse_variable(self):
        node = Variable(self.current_token)
        self.eat(TOKEN_TYPES.ID.value)
        return node


    def parse_empty(self):
        return EmptyOperation()


    def make_parse(self):
        node = self.parse_program()

        if self.current_token.type != TOKEN_TYPES.EOF.value:
            self.error()

        return node

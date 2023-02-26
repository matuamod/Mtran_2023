from .AST import *
from ..lexical_analyzer import TOKEN_TYPES


class SyntaxAnalyzer(object):

    def __init__(self, lexical_analyzer):
        # lexical_analyzer initialization
        self.lexical_analyzer = lexical_analyzer
        # Current token instance
        self.current_token = self.lexical_analyzer.getNextToken()


    def error(self):
        raise Exception("Error. Invalid syntax")


    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexical_analyzer.getNextToken()
        else:
            self.error()


    def paren(self):
        self.eat(TOKEN_TYPES.LPAREN.value)
        node = self.expr()
        self.eat(TOKEN_TYPES.RPAREN.value)
        return node


    def factor(self):
        token = self.current_token

        if token.type == TOKEN_TYPES.PLUS.value:
            self.eat(TOKEN_TYPES.PLUS.value)
            return UnaryOperation(
                token=token,
                expr=self.factor()
            )
        elif token.type == TOKEN_TYPES.MINUS.value:
            self.eat(TOKEN_TYPES.MINUS.value)
            return UnaryOperation(
                token=token,
                expr=self.factor()
            )
        elif token.type == TOKEN_TYPES.INTEGER.value:
            self.eat(TOKEN_TYPES.INTEGER.value)
            return Number(token)
        elif token.type == TOKEN_TYPES.LPAREN.value:
            return self.paren()
        else:
            return self.variable() 


    def temp(self):
        node = self.factor()

        while self.current_token.type in (
                TOKEN_TYPES.MUL.value,
                TOKEN_TYPES.DIV.value):

            token = self.current_token

            if self.current_token.type == TOKEN_TYPES.MUL.value:
                self.eat(TOKEN_TYPES.MUL.value)
            elif self.current_token.type == TOKEN_TYPES.DIV.value:
                self.eat(TOKEN_TYPES.DIV.value)

            node = BinaryOperation(
                left_node=node,
                token=token,
                right_node=self.factor()
            )

        return node


    def expr(self):
        node = self.temp()

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
                right_node=self.temp()
            )

        return node


    def program(self):
        node = self.compoundStatement()
        self.eat(TOKEN_TYPES.DOT.value)
        return node


    def compoundStatement(self):
        self.eat(TOKEN_TYPES.BEGIN.value)
        nodes_list = self.statementList()
        self.eat(TOKEN_TYPES.END.value)

        compound_statement = CompoundStatement()

        for node in nodes_list:
            compound_statement.statement_list.append(node)  

        return compound_statement 


    def statementList(self):
        statement_list = list()
        node = self.statement()
        statement_list.append(node)

        while self.current_token.type == TOKEN_TYPES.SEMICOLON.value:
            self.eat(TOKEN_TYPES.SEMICOLON.value)
            print(self.current_token.value)
            statement_list.append(self.statement())

        if self.current_token.type == TOKEN_TYPES.ID.value:
            self.error()

        return statement_list


    def statement(self):
        if self.current_token.type == TOKEN_TYPES.BEGIN.value:
            node = self.compoundStatement()
        elif self.current_token.type == TOKEN_TYPES.ID.value:
            node = self.assignmentStatement()
        else:
            node = self.empty()

        return node


    def assignmentStatement(self):
        left_node = self.variable()
        token = self.current_token
        self.eat(TOKEN_TYPES.ASSINGMENT.value)
        right_node = self.expr()

        node = AssignmentStatement(left_node, token, right_node)
        return node


    def variable(self):
        node = Variable(self.current_token)
        self.eat(TOKEN_TYPES.ID.value)
        return node


    def empty(self):
        return EmptyOperation()


    def makeParse(self):
        node = self.program()

        if self.current_token.type != TOKEN_TYPES.EOF.value:
            self.error()

        return node

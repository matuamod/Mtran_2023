import re
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
            
        if re.match(r'\+|\-', str(token.value)):
            self.eat(token.type)

            return UnaryOperation(
                token=token,
                expr=self.parse_factor()
            )
        
        elif str(token.type).endswith("_CONST"):
            self.eat(token.type)

            if re.match(r'(\d+(?:\.\d+)?)', str(token.value)):
                return Number(token=token)
            elif re.match(r'([A-Za-z\_\d+])+', str(token.value)):
                return Literal(token=token)
            
        elif token.type == TOKEN_TYPES.LPAREN.value:
            return self.parse_paren()
        
        else:
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
        self.eat(TOKEN_TYPES.PROGRAM.value)
        variable_node = self.parse_variable()
        name = variable_node.value
        self.eat(TOKEN_TYPES.SEMICOLON.value)
        block_node = self.parse_block()
        self.eat(TOKEN_TYPES.DOT.value)

        program = Program(
            name=name, 
            block=block_node
            )
         
        return program
    

    def parse_block(self):
        declaration_node = self.parse_declaration()
        compound_statement_node = self.parse_compound_statement()

        block = Block(
            declaration=declaration_node, 
            compound_statement=compound_statement_node
            )
        
        return block


    def parse_declaration(self):
        if self.current_token.type == TOKEN_TYPES.VAR.value:
            self.eat(TOKEN_TYPES.VAR.value)

            declaration = Declaration()

            # Iteration is actual for current line in VAR statement
            while self.current_token.type == TOKEN_TYPES.ID.value:
                var_declaration = self.parse_variable_declaration()
                declaration.declaration_list.extend(var_declaration)
                self.eat(TOKEN_TYPES.SEMICOLON.value)

        return declaration


    def parse_variable_declaration(self):
        variable_list = list()
        declaration_list = list()
        variable_list.append(self.parse_variable())

        while self.current_token.type == TOKEN_TYPES.COMMA.value:
            self.eat(TOKEN_TYPES.COMMA.value)
            variable_list.append(self.parse_variable())

        self.eat(TOKEN_TYPES.COLON.value)

        type_node = self.parse_type_spec()

        for variable_node in variable_list:
            declaration_list.append(VariableDeclaration(
                variable_node=variable_node, 
                type_node=type_node
            ))

        return declaration_list


    def parse_type_spec(self):
        token = self.current_token
        self.eat(token.type)

        type_node = Type(token=token)
        return type_node


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

            # TODO : Add parse comparison and change statements

            case TOKEN_TYPES.READLN.value:
                node = self.parse_input_statement()

            case TOKEN_TYPES.WRITELN.value:
                node = self.parse_output_statement()
                 
            case _:
                node = self.parse_empty()

        return node


    def parse_assignment_statement(self):
        left_node = self.parse_variable()
        token = self.current_token
        """Eat all assignment sign"""
        self.eat(token.type)
        right_node = self.parse_expr()

        node = AssignmentStatement(
            left_node=left_node, 
            token=token, 
            right_node=right_node
            )
        
        return node
    

    def parse_comparison_statement(self):
        left_node = self.parse_expr()
        token = self.current_token
        """eat all comparison sign"""
        self.eat(token.type)
        right_node = self.parse_expr()

        node = ComparisonStatement(
            left_node=left_node, 
            token=token, 
            right_node=right_node
        )

        return node
    

    def parse_input_statement(self):
        self.eat(TOKEN_TYPES.READLN.value)
        self.eat(TOKEN_TYPES.LPAREN.value)

        input_statement = InputStatement()
        input_statement.input_list.append(self.parse_expr())

        while self.current_token.type == TOKEN_TYPES.COMMA.value:
            self.eat(TOKEN_TYPES.COMMA.value)
            input_statement.input_list.append(self.parse_expr())

        self.eat(TOKEN_TYPES.RPAREN.value)
        return input_statement


    def parse_output_statement(self):
        print(self.current_token.value)
        self.eat(TOKEN_TYPES.WRITELN.value)
        print(self.current_token.value)
        self.eat(TOKEN_TYPES.LPAREN.value)

        output_statement = OutputStatement()
        output_statement.output_list.append(self.parse_expr())

        while self.current_token.type == TOKEN_TYPES.COMMA.value:
            self.eat(TOKEN_TYPES.COMMA.value)
            output_statement.output_list.append(self.parse_expr())

        self.eat(TOKEN_TYPES.RPAREN.value)
        return output_statement
    

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

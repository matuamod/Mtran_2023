import re
from .AST import *
from ..lexical_analyzer import TOKEN_TYPES, ConfigureTables
from .syntax_error import SyntaxError, ErrorTypes


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

    
    def error(self, message):
        raise SyntaxError(self.lexical_analyzer.line_num, self.lexical_analyzer.column_num, message)


    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexical_analyzer.get_next_token()
            self.conf.fill_table(self.current_token)
        else:
            self.error(ErrorTypes.STANDART_ERROR.value)


    def parse_program(self):
        self.eat(TOKEN_TYPES.PROGRAM.value)
        variable_node = self.parse_variable()
        name = variable_node.value
        
        if self.current_token.type != TOKEN_TYPES.SEMICOLON.value:
            self.error(ErrorTypes.SEMICOLON_ERROR.value)
            
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
        declaration = Declaration()
        
        if self.current_token.type == TOKEN_TYPES.VAR.value:
            self.eat(TOKEN_TYPES.VAR.value)

            # Iteration is actual for current line in VAR statement
            while self.current_token.type == TOKEN_TYPES.ID.value or \
                self.current_token.type == TOKEN_TYPES.PROCEDURE.value:

                if self.current_token.type == TOKEN_TYPES.ID.value:
                    var_declaration = self.parse_variable_declaration()
                    declaration.declaration_list.extend(var_declaration)
                    
                    if self.current_token.type != TOKEN_TYPES.SEMICOLON.value:
                        self.error(ErrorTypes.SEMICOLON_ERROR.value)
                    
                    self.eat(TOKEN_TYPES.SEMICOLON.value)
                elif self.current_token.type == TOKEN_TYPES.PROCEDURE.value:
                    proc_declaration = self.parse_procedure_declaration()
                    declaration.declaration_list.extend(proc_declaration)

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


    def parse_procedure_declaration(self):
        declaration_list = list()

        if self.current_token.type == TOKEN_TYPES.VAR.value:
            self.eat(TOKEN_TYPES.VAR.value)

            while self.current_token.type == TOKEN_TYPES.ID.value:
                var_declaration = self.parse_variable_declaration()
                declaration_list.extend(var_declaration)

        while self.current_token.type == TOKEN_TYPES.PROCEDURE.value:
            self.eat(TOKEN_TYPES.PROCEDURE.value)
            name = self.parse_variable()
            
            if self.current_token.type != TOKEN_TYPES.SEMICOLON.value:
                self.error(ErrorTypes.SEMICOLON_ERROR.value)

            self.eat(TOKEN_TYPES.SEMICOLON.value)
            block_node = self.parse_block()

            proc_declaration =  ProcedureDeclaration(
                name=name,
                block=block_node
            )

            declaration_list.append(proc_declaration)
            
            if self.current_token.type != TOKEN_TYPES.SEMICOLON.value:
                self.error(ErrorTypes.SEMICOLON_ERROR.value)
            
            self.eat(TOKEN_TYPES.SEMICOLON.value)
            
        return declaration_list


    def parse_type_spec(self):
        token = self.current_token
        
        if token.type not in (
            TOKEN_TYPES.INTEGER.value, TOKEN_TYPES.REAL.value,
            TOKEN_TYPES.CHAR.value, TOKEN_TYPES.STRING.value,
            TOKEN_TYPES.BOOLEAN.value
        ):
            self.error(ErrorTypes.TYPE_ERROR.value)
        else: 
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
            self.error(ErrorTypes.IDENTIFIER_ERROR.value)

        return statement_list


    def parse_statement(self):
        match self.current_token.type:
            case TOKEN_TYPES.BEGIN.value:
                node = self.parse_compound_statement()

            case TOKEN_TYPES.ID.value:
                 node = self.parse_assignment_statement()

            case TOKEN_TYPES.READLN.value:
                node = self.parse_input_statement()

            case TOKEN_TYPES.WRITELN.value:
                node = self.parse_output_statement()

            case TOKEN_TYPES.IF.value:
                node = self.parse_if_statement()
                
            case TOKEN_TYPES.CASE.value:
                node = self.parse_case_statement()
                 
            case _:
                
                if self.current_token.type in (
                    TOKEN_TYPES.EXIT.value,
                    TOKEN_TYPES.CONTINUE.value,
                    TOKEN_TYPES.BREAK.value
                ):
                    node = self.parse_jump_statement()
                elif self.current_token.type in (
                    TOKEN_TYPES.FOR.value,
                    TOKEN_TYPES.WHILE.value,
                    TOKEN_TYPES.REPEAT.value
                ):
                    node = self.parse_loop_statement()
                else:
                    node = self.parse_empty()

        return node


    def parse_assignment_statement(self):
        left_node = self.parse_variable()
        token = self.current_token
        """Eat all assignment sign"""
        
        if token.type != TOKEN_TYPES.ASSINGMENT.value:
            self.error(ErrorTypes.ASSIGNMENT_ERRROR.value)
        else:
            self.eat(token.type)
            right_node = self.parse_logic()

            node = AssignmentStatement(
                left_node=left_node, 
                token=token, 
                right_node=right_node
                )
        
        return node
        

    def parse_input_statement(self):
        self.eat(TOKEN_TYPES.READLN.value)
        self.eat(TOKEN_TYPES.LPAREN.value)

        input_statement = InputStatement()
        input_statement.input_list.append(self.parse_logic())

        while self.current_token.type == TOKEN_TYPES.COMMA.value:
            self.eat(TOKEN_TYPES.COMMA.value)
            input_statement.input_list.append(self.parse_logic())

        self.eat(TOKEN_TYPES.RPAREN.value)
        return input_statement


    def parse_output_statement(self):
        self.eat(TOKEN_TYPES.WRITELN.value)
        self.eat(TOKEN_TYPES.LPAREN.value)

        output_statement = OutputStatement()
        output_statement.output_list.append(self.parse_logic())

        while self.current_token.type == TOKEN_TYPES.COMMA.value:
            self.eat(TOKEN_TYPES.COMMA.value)
            output_statement.output_list.append(self.parse_logic())

        self.eat(TOKEN_TYPES.RPAREN.value)
        return output_statement
    

    def parse_if_statement(self):
        self.eat(TOKEN_TYPES.IF.value)
        condition = self.parse_comparison()
        self.eat(TOKEN_TYPES.THEN.value)
        statement = self.parse_statement()

        if self.current_token.type == TOKEN_TYPES.ELSE.value:
            self.eat(TOKEN_TYPES.ELSE.value)
            next_statement = self.parse_statement()

            if_statement = IfStatement(
                comparison=condition,
                statement=statement,
                next_statement=next_statement
            )
        else:
            if_statement = IfStatement(
                comparison=condition,
                statement=statement
            )

        return if_statement
    
    
    def parse_loop_statement(self):
        match(self.current_token.type):
            case TOKEN_TYPES.FOR.value:
                self.eat(TOKEN_TYPES.FOR.value)
                assignment = self.parse_statement()
                self.eat(TOKEN_TYPES.TO.value)
                border = self.parse_logic()
                self.eat(TOKEN_TYPES.DO.value)
                statement = self.parse_statement()
                
                return ForLoop(
                    assignment=assignment,
                    border=border,
                    statement=statement
                )
                
            case TOKEN_TYPES.WHILE.value:
                self.eat(TOKEN_TYPES.WHILE.value)
                border = self.parse_comparison()
                print(self.current_token.type)
                self.eat(TOKEN_TYPES.DO.value)
                print(self.current_token.type)
                statement = self.parse_statement()
                
                return WhileLoop(
                    border=border,
                    statement=statement
                )
                
            case TOKEN_TYPES.REPEAT.value:
                self.eat(TOKEN_TYPES.REPEAT.value)
                statement = self.parse_statement()
                self.eat(TOKEN_TYPES.UNTIL.value)
                border = self.parse_comparison()
                
                return RepeatLoop(
                    statement=statement,
                    border=border
                )
                    
    
    def parse_jump_statement(self):
        expr = None
        
        match self.current_token.type:
            case TOKEN_TYPES.EXIT.value:
                jump = "Exit"
                self.eat(TOKEN_TYPES.EXIT.value)
                self.eat(TOKEN_TYPES.LPAREN.value)
                
                if self.current_token.type == TOKEN_TYPES.RPAREN.value:
                    self.eat(TOKEN_TYPES.RPAREN.value)
                else:
                    expr = self.parse_logic()
                    self.eat(TOKEN_TYPES.RPAREN.value)
                    
            case TOKEN_TYPES.CONTINUE.value:
                jump = "Continue"
                self.eat(TOKEN_TYPES.CONTINUE.value)
                
            case TOKEN_TYPES.BREAK.value:
                jump = "Break"
                self.eat(TOKEN_TYPES.BREAK.value)
                
        jump_statement = JumpStatement(
            jump=jump,
            expr=expr
        )
        
        return jump_statement
    
    
    def parse_case_statement(self):
        self.eat(TOKEN_TYPES.CASE.value)
        condition = self.parse_logic()
        self.eat(TOKEN_TYPES.OF.value)
        
        case_list = list()
        case_list.append(self.parse_case_compound())
        
        while self.current_token.type == TOKEN_TYPES.SEMICOLON.value:
            self.eat(TOKEN_TYPES.SEMICOLON.value)
            
            if self.current_token.type == TOKEN_TYPES.END.value:
                break
            
            if self.current_token.type == TOKEN_TYPES.ELSE.value:
                case_list.append(self.parse_default_compound())
                
                case_statement = CaseStatement(
                    condition=condition,
                    case_list=case_list
                )
                
                if self.current_token.type != TOKEN_TYPES.SEMICOLON.value:
                    self.error(ErrorTypes.SEMICOLON_ERROR.value)
                
                self.eat(TOKEN_TYPES.SEMICOLON.value)
                self.eat(TOKEN_TYPES.END.value)
                return case_statement
            
            case_list.append(self.parse_case_compound())
            
        case_statement = CaseStatement(
            condition=condition,
            case_list=case_list
        )    
        
        self.eat(TOKEN_TYPES.END.value)         
        return case_statement
    
    
    def parse_case_compound(self):
        case = self.parse_logic()
        self.eat(TOKEN_TYPES.COLON.value)
        result = self.parse_statement()
        
        case_compound = CaseCompound(
            case=case,
            result=result
        )
        
        return case_compound
    
    
    def parse_default_compound(self):
        default = "Else"
        self.eat(TOKEN_TYPES.ELSE.value)
        result = self.parse_statement()
        
        default_compound = DefaultCompound(
            default=default,
            result=result
        )
        
        return default_compound
    

    def parse_comparison(self):
        node = self.parse_logic()

        while self.current_token.type.endswith("EQUAL") or \
            self.current_token.type in (
                TOKEN_TYPES.GREATER.value,
                TOKEN_TYPES.LESS.value
            ):
            token = self.current_token
            """eat all comparison sign"""
            self.eat(token.type)

            node = ComparisonStatement(
                left_node=node, 
                token=token, 
                right_node=self.parse_logic()
            )

        return node
    
    
    def parse_logic(self):
        node = self.parse_expr()
        
        while self.current_token.type in (
                TOKEN_TYPES.OR.value,
                TOKEN_TYPES.AND.value,
                TOKEN_TYPES.XOR.value):
            
            token = self.current_token
            self.eat(token.type)
                    
            node = LogicalOperation(
                left_node=node,
                token=token,
                right_node=self.parse_expr()
            )
            
        return node
    

    def parse_expr(self):
        node = self.parse_term()

        while self.current_token.type in (
                TOKEN_TYPES.MINUS.value,
                TOKEN_TYPES.PLUS.value):

            token = self.current_token
            self.eat(token.type)

            node = BinaryOperation(
                left_node=node,
                token=token,
                right_node=self.parse_term()
            )

        return node
    

    def parse_term(self):
        node = self.parse_factor()

        while self.current_token.type in (
                TOKEN_TYPES.MUL.value,
                TOKEN_TYPES.FLOAT_DIV.value,
                TOKEN_TYPES.INTEGER_DIV.value):

            token = self.current_token
            self.eat(token.type)
            
            node = BinaryOperation(
                left_node=node,
                token=token,
                right_node=self.parse_factor()
            )

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
            else:
                self.error(ErrorTypes.CONSTANT_ERROR.value)
                 
        elif token.type == TOKEN_TYPES.LPAREN.value:
            return self.parse_paren()
        
        else:
            return self.parse_variable()

    
    def parse_paren(self):
        self.eat(TOKEN_TYPES.LPAREN.value)
        node = self.parse_expr()
        self.eat(TOKEN_TYPES.RPAREN.value)
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
            self.error(ErrorTypes.STANDART_ERROR.value)

        return node

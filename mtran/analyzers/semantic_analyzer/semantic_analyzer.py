from .semantic_error import SemanticError, ErrorTypes
from ..syntax_analyzer import AST_Visitor
from ..lexical_analyzer import TOKEN_TYPES
from .symbols import ScopedSymbolTable, Symbol, VariableSymbol, BuiltinTypeSymbol, ProcedureSymbol, FunctionSymbol

class SemanticAnalyzer(AST_Visitor):
    
    def __init__(self, ast_tree):
        super().__init__(ast_tree)
        # First scope before global
        self.current_scope = None
        
        
    def error(self, addition, message):
        raise SemanticError(addition, message)
        
            
    def visit_program(self, node):
        global_scope = ScopedSymbolTable(
            scope_name="global",
            scope_level=1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = global_scope
        self.visit_block(node.block)
        self.current_scope = self.current_scope.enclosing_scope
        print(global_scope)
    
    
    def visit_block(self, node):
        self.visit_node(node.declaration)
        self.visit_node(node.compound_statement)
        
        
    def visit_declaration(self, node):
        for declaration in node.declaration_list:
            self.visit_node(declaration)
            
    
    def visit_variable_declaration(self, node):
        variable_name = node.variable_node.value
        type_name = node.type_node.value
        
        if self.current_scope.lookup(type_name) is None:
            type_symbol = BuiltinTypeSymbol(type_name)
            self.current_scope.insert(type_symbol)
            
        type_symbol = self.current_scope.lookup(type_name)        
        
        if self.current_scope.lookup(variable_name, True):
            self.error(
                addition=f"Dublicate identifier '{variable_name}' was found",
                message=ErrorTypes.DUBLICATE_ERROR.value
            )
        
        variable_symbol = VariableSymbol(variable_name, type_symbol)
        node.variable_node.variable_type = type_symbol.name
        
        self.current_scope.insert(variable_symbol)
                
        
    def visit_procedure_declaration(self, node):
        procedure_name = node.name.value
        procedure_symbol = ProcedureSymbol(name=procedure_name)
        self.current_scope.insert(procedure_symbol)
                
        procedure_scope = ScopedSymbolTable(
            scope_name=procedure_name,
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = procedure_scope
        
        if node.params:
            for param in node.params:
                self.visit_variable_declaration(param)
                procedure_symbol.params.append(
                    self.current_scope.lookup(param.variable_node.value))
        
        self.visit_node(node.block_node)
        procedure_symbol.block = node.block_node
        
        self.current_scope = self.current_scope.enclosing_scope
        
        print(procedure_scope)
        
        
    def visit_function_declaration(self, node):
        function_name = node.name.value
        function_type = node.ret_type
        function_symbol = FunctionSymbol(name=function_name, ret_type=function_type)
        self.current_scope.insert(function_symbol)
                
        function_scope = ScopedSymbolTable(
            scope_name=function_name,
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = function_scope
        
        if node.params:
            for param in node.params:
                self.visit_variable_declaration(param)
                function_symbol.params.append(
                    self.current_scope.lookup(param.variable_node.value))
        
        self.visit_node(node.block_node)
        function_symbol.block = node.block_node
        
        self.current_scope = self.current_scope.enclosing_scope
        
        print(function_scope)
        
        
    def visit_compound_statement(self, node):
        for statement in node.statement_list:
            self.visit_node(statement)
            
            
    def visit_call(self, node):        
        for param_node in node.actual_params:
            self.visit_node(param_node)
            
        symbol = self.current_scope.lookup(node.name.value)
        
        if symbol.name == self.current_scope.scope_name:
            symbol = self.current_scope.enclosing_scope.lookup(node.name.value)
        
        node.symbol = symbol
        
        if symbol.__class__.__name__ == "FunctionSymbol":
            return symbol.ret_type
            
            
    def visit_case_compound(self, node):
        case_type = self.visit_node(node.case)
        self.visit_node(node.result)
        return case_type
    
    
    def visit_default_compound(self, node):
        self.visit_node(node.result)
    
    
    def visit_assignment_statement(self, node):
        left_type = self.visit_node(node.left_node)
        right_type = self.visit_node(node.right_node)
        
        if left_type != right_type:
            if node.left_node.__class__.__name__ == "CallStatement":
                self.error(
                    addition=f"Can't assign '{node.left_node.name.value}': {left_type}" +
                        f" with '{node.right_node.value}': {right_type}",
                    message=ErrorTypes.ASSIGNMENT_ERRROR.value 
                )
            if node.right_node.__class__.__name__ == "CallStatement":
                self.error(
                    addition=f"Can't assign '{node.left_node.value}': {left_type}" +
                        f" with '{node.right_node.name.value}': {right_type}",
                    message=ErrorTypes.ASSIGNMENT_ERRROR.value 
                )
            else: self.error(
                    addition=f"Can't assign '{node.left_node.value}': {left_type}" +
                        f" with '{node.right_node.value}': {right_type}",
                    message=ErrorTypes.ASSIGNMENT_ERRROR.value 
                )
            
        return left_type  
    
    
    def visit_jump_statement(self, node):
        if node.expr is not None:
            self.visit_node(node.expr)
    
    
    def visit_case_statement(self, node):
        condition_type = self.visit_node(node.condition)
        
        for case in node.case_list:
            case_type = self.visit_node(case)
            
            if condition_type != case_type and case_type is not None:
                self.error(
                    addition=f"Can't execute condition {node.condition.value}: '{condition_type}'" + \
                        f" with case compound {case.case.value}: {case_type}",
                        message=ErrorTypes.CASE_COMPOUND_ERROR.value
                )
    
    
    def visit_comparison(self, node):
        left_type = self.visit_node(node.left_node)
        right_type = self.visit_node(node.right_node)
        
        number_types = (TOKEN_TYPES.INTEGER.value,
                        TOKEN_TYPES.REAL.value)
        
        if left_type == right_type or \
            left_type in number_types and \
                right_type in number_types:
            return TOKEN_TYPES.BOOLEAN.value
        else:
            operation = f"make '{node.operation.type.lower()}' operation"
            
            if node.left_node.__class__.__name__ == "CallStatement":
                self.error(
                addition=f"Can't {operation} for '{node.left_node.name.value}': {left_type}" +
                    f" with '{node.right_node.value}': {right_type}",
                message=ErrorTypes.COMPARISON_ERROR.value 
                )
            elif node.right_node.__class__.__name__ == "CallStatement":
                self.error(
                addition=f"Can't {operation} for '{node.left_node.value}': {left_type}" +
                    f" with '{node.right_node.value.value}': {right_type}",
                message=ErrorTypes.COMPARISON_ERROR.value 
                )
            else: self.error(
                    addition=f"Can't {operation} for '{node.left_node.value}': {left_type}" +
                        f" with '{node.right_node.value}': {right_type}",
                    message=ErrorTypes.COMPARISON_ERROR.value 
                )
    
    
    def visit_input_statement(self, node):
        for input in node.input_list:
            
            if input.__class__.__name__ == "Variable":
                self.visit_node(input)
            else: 
                self.error(
                    addition=f"Can't pass argument: '{input.token.value}'" + \
                        f" with type: '{input.__class__.__name__}'",
                    message=ErrorTypes.INPUT_ERROR.value
                )
    
    
    def visit_output_statement(self, node):
        for output in node.output_list:
            self.visit_node(output)
    
    
    def visit_if_statement(self, node):
        condition_type = self.visit_node(node.comparison)
        
        if condition_type == TOKEN_TYPES.BOOLEAN.value:
            self.visit_node(node.statement)
            
            if node.next_statement is not None:
                self.visit_node(node.next_statement)
        else:
            self.error(
                addition=f"Condition type is not BOOLEAN, but: '{condition_type}'",
                message=ErrorTypes.IF_COMPARISON_ERROR.value
            )
    
    
    def visit_for_statement(self, node):
        assignment_type = self.visit_node(node.assignment[0])
        border_type = self.visit_node(node.border[0])
        
        if assignment_type == border_type and \
            assignment_type == TOKEN_TYPES.INTEGER.value and \
                border_type == TOKEN_TYPES.INTEGER.value:
            self.visit_node(node.statement)
        else: 
            self.error(
                addition=f"Check execution conditions. Assignment type: {assignment_type}, " + 
                f"border type: {border_type}",
                message=ErrorTypes.FOR_LOOP_ERROR.value
            )
    
    
    def visit_while_statement(self, node):
        border_type = self.visit_node(node.border)
        
        if border_type == TOKEN_TYPES.BOOLEAN.value:
            self.visit_node(node.statement)
        else:
            self.error(
                addition=f"Check execution conditions. Condition type: {border_type}",
                message=ErrorTypes.WHILE_LOOP_ERROR.value
            )
    
    
    def visit_repeat_statement(self, node):
        self.visit_node(node.statement[0])
        border_type = self.visit_node(node.border)
        
        if border_type != TOKEN_TYPES.BOOLEAN.value:
            self.error(
                addition=f"check execution conditions. Condition type: {border_type}",
                message=ErrorTypes.UNTIL_LOOP_ERROR.value
            )
    
    
    def visit_variable(self, node):
        variable_name = node.value
        variable_symbol = self.current_scope.lookup(variable_name)
    
        if variable_symbol is None:
            self.error(
                addition=f"Symbol(identifier) was not found: '{variable_name}'",
                message=ErrorTypes.SYMBOL_ERROR.value
            )
                
        node.variable_type = variable_symbol.type.name
            
        return variable_symbol.type.name
        
    
    def visit_logical_operation(self, node):
        left_type = self.visit_node(node.left_node)
        right_type = self.visit_node(node.right_node)
        
        if left_type != right_type:
            operation = f"make '{node.operation.type.lower()}' operation"
            
            if node.left_node.__class__.__name__ == "CallStatement":
                self.error(
                    addition=f"Can't {operation} for '{node.left_node.name.value}': {left_type}" +
                        f" with '{node.right_node.value}': {right_type}",
                    message=ErrorTypes.LOGICAL_OP_ERROR.value
                )
            elif  node.right_node.__class__.__name__ == "CallStatement":
                self.error(
                    addition=f"Can't {operation} for '{node.left_node.value}': {left_type}" +
                        f" with '{node.right_node.name.value}': {right_type}",
                    message=ErrorTypes.LOGICAL_OP_ERROR.value
                )
            else: self.error(
                    addition=f"Can't {operation} for '{node.left_node.value}': {left_type}" +
                        f" with '{node.right_node.value}': {right_type}",
                    message=ErrorTypes.LOGICAL_OP_ERROR.value 
                )
            
        return TOKEN_TYPES.BOOLEAN.value
    
    
    def visit_binary_operation(self, node):
        left_type = self.visit_node(node.left_node)
        right_type = self.visit_node(node.right_node)
        
        match (left_type):
            case TOKEN_TYPES.INTEGER.value:
                if right_type == TOKEN_TYPES.INTEGER.value:
                    return TOKEN_TYPES.INTEGER.value
                elif right_type == TOKEN_TYPES.REAL.value:
                    return TOKEN_TYPES.REAL.value

            case TOKEN_TYPES.REAL.value:
                if right_type == TOKEN_TYPES.INTEGER.value or \
                    right_type == TOKEN_TYPES.REAL.value:
                    return TOKEN_TYPES.REAL.value
               
            case TOKEN_TYPES.CHAR.value:
                if node.operation.type == TOKEN_TYPES.PLUS.value:
                    
                    if right_type == TOKEN_TYPES.CHAR.value or \
                        right_type == TOKEN_TYPES.STRING.value:
                        return TOKEN_TYPES.STRING.value
            
            case TOKEN_TYPES.STRING.value:
                 if node.operation.type == TOKEN_TYPES.PLUS.value:
                    
                    if right_type == TOKEN_TYPES.CHAR.value or \
                        right_type == TOKEN_TYPES.STRING.value:
                        return TOKEN_TYPES.STRING.value 
        
        operation = f"make '{node.operation.type.lower()}' operation"
        
        print(node.left_node.__class__.__name__)
        
        if node.left_node.__class__.__name__ == "CallStatement":
            self.error(
                addition=f"Can't {operation} for '{node.left_node.name.value}': {left_type}" +
                    f" with '{node.right_node.value}': {right_type}",
                message=ErrorTypes.BINARY_OP_ERROR.value 
            )
        elif node.right_node.__class__.__name__ == "CallStatement":
            self.error(
                addition=f"Can't {operation} for '{node.left_node.value}': {left_type}" +
                    f" with '{node.right_node.name.value}': {right_type}",
                message=ErrorTypes.BINARY_OP_ERROR.value 
            )
        else: self.error(
                addition=f"Can't {operation} for '{node.left_node.value}': {left_type}" +
                    f" with '{node.right_node.value}': {right_type}",
                message=ErrorTypes.BINARY_OP_ERROR.value 
            )  
        
    
    def visit_unary_operation(self, node):
        return self.visit_node(node.expr)
        
        
    def visit_literal(self, node):
        return node.token.type.partition("_CONST")[0]
    
    
    def visit_number(self, node):
        return node.token.type.partition("_CONST")[0]
    
    
    def visit_empty_operation(self, node):
        pass
    
    
    def visit_type_dec(self, node):
        pass
       
            
    def check_ast(self):
        self.start_visit()
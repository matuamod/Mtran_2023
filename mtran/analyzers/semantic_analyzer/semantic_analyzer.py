from .semantic_error import SemanticError, ErrorTypes
from ..syntax_analyzer import AST_Visitor
from ..lexical_analyzer import TOKEN_TYPES
from .symbols import SymbolTable, Symbol, VariableSymbol, BuiltinTypeSymbol

class SemanticAnalyzer(AST_Visitor):
    
    def __init__(self, ast_tree):
        super().__init__(ast_tree)
        self.symbol_table = SymbolTable()
        
        
    def error(self, addition, message):
        raise SemanticError(addition, message)
        
            
    def visit_program(self, node):
        self.visit_block(node.block)
    
    
    def visit_block(self, node):
        self.visit_node(node.declaration)
        self.visit_node(node.compound_statement)
        
        
    def visit_declaration(self, node):
        for declaration in node.declaration_list:
            self.visit_node(declaration)
            
    
    def visit_variable_declaration(self, node):
        variable_name = node.variable_node.value
        type_name = node.type_node.value
        
        if self.symbol_table.lookup(type_name) is None:
            type_symbol = BuiltinTypeSymbol(type_name)
            self.symbol_table.insert(type_symbol)
            
        type_symbol = self.symbol_table.lookup(type_name)        
        
        if self.symbol_table.lookup(variable_name) is not None:
            self.error(
                addition=f"Dublicate identifier '{variable_name}' was found",
                message=ErrorTypes.DUBLICATE_ERROR.value
            )
        
        variable_symbol = VariableSymbol(variable_name, type_symbol)
        self.symbol_table.insert(variable_symbol)
                
        
    def visit_procedure_declaration(self, node):
        self.visit_node(node.block_node)
    

    def visit_compound_statement(self, node):
        for statement in node.statement_list:
            self.visit_node(statement)
            
            
    def visit_case_compound(self, node):
        self.visit_node(node.case)
        self.visit_node(node.result)
    
    
    def visit_default_compound(self, node):
        self.visit_node(node.result)
    
    
    def visit_assignment_statement(self, node):
        left_type = self.visit_node(node.left_node)
        right_type = self.visit_node(node.right_node)
        
        if left_type != right_type:
            self.error(
                addition=f"Can't assign '{node.left_node.value}': {left_type}" +
                    f" with '{node.right_node.value}': {right_type}",
                message=ErrorTypes.ASSIGNMENT_ERRROR.value 
            )  
    
    
    def visit_jump_statement(self, node):
        if node.expr is not None:
            self.visit_node(node.expr)
    
    
    def visit_case_statement(self, node):
        self.visit_node(node.condition)
        
        for case in node.case_list:
            self.visit_node(case)
    
    
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
            self.error(
                addition=f"Can't {operation} for '{node.left_node.value}': {left_type}" +
                    f" with '{node.right_node.value}': {right_type}",
                message=ErrorTypes.COMPARISON_ERROR.value 
            )
    
    
    def visit_input_statement(self, node):
        for input in node.input_list:
            self.visit_node(input)
    
    
    def visit_output_statement(self, node):
        for output in node.output_list:
            self.visit_node(output)
    
    
    def visit_if_statement(self, node):
        self.visit_node(node.comparison)
        self.visit_node(node.statement)
        
        if node.next_statement is not None:
            self.visit_node(node.next_statement)
    
    
    def visit_for_statement(self, node):
        self.visit_node(node.assgnment[0])
        self.visit_node(node.border[0])
        self.visit_node(node.statement)
    
    
    def visit_while_statement(self, node):
        self.visit_node(node.border)
        self.visit_node(node.statement)
    
    
    def visit_repeat_statement(self, node):
        self.visit_node(node.statement[0])
        self.visit_node(node.border)
    
    
    def visit_variable(self, node):
        variable_name = node.value
        variable_symbol = self.symbol_table.lookup(variable_name)
    
        if variable_symbol is None:
            self.error(
                addition=f"Symbol(identifier) was not found: '{variable_name}'",
                message=ErrorTypes.SYMBOL_ERROR.value
            )
            
        return variable_symbol.type.name
        
    
    def visit_logical_operation(self, node):
        left_type = self.visit_node(node.left_node)
        right_type = self.visit_node(node.right_node)
        
        if left_type != right_type:
            operation = f"make '{node.operation.type.lower()}' operation"
            self.error(
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
        self.error(
            addition=f"Can't {operation} for '{node.left_node.value}': {left_type}" +
                f" with '{node.right_node.value}': {right_type}",
            message=ErrorTypes.BINARY_OP_ERROR.value 
        )  
        
    
    def visit_unary_operation(self, node):
        self.visit_node(node.expr)
        
        
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
        print(self.symbol_table)
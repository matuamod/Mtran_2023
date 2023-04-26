from operator import xor
from analyzers import TOKEN_TYPES
from analyzers.syntax_analyzer import AST_Visitor
from .stack import CallStack, Record, RecordType

class Interpreter(AST_Visitor):

    def __init__(self, ast_tree):
        super().__init__(ast_tree)
        self.ast_tree = ast_tree
        self.call_stack = CallStack()
        
        
    def visit_program(self, node):
        program_name = node.name
        print(f"Enter PROGRAM {program_name}")
        
        record = Record(
            name=program_name,
            type=RecordType.PROGRAM.value,
            nesting_level=1
        )
        
        self.call_stack.push(record)
        self.visit_node(node.block)
        self.call_stack.pop()
        print(f"Leave PROGRAM {program_name}")
    
    
    def visit_block(self, node):
        self.visit_node(node.declaration)
        self.visit_node(node.compound_statement)
    
    
    def visit_declaration(self, node):
        for declaration in node.declaration_list:
            self.visit_node(declaration)
    
    
    def visit_variable_declaration(self, node):
        self.visit_node(node.variable_node)
        self.visit_node(node.type_node)
    
    
    def visit_procedure_declaration(self, node):
        pass
    

    def visit_compound_statement(self, node):
        for statement in node.statement_list:
            self.visit_node(statement)
            
            
    def visit_procedure_call(self, node):
        procedure_name = node.procedure_name.value
        curr_nesting_level = self.call_stack.peek().nesting_level
        
        record = Record(
            name=procedure_name,
            type=RecordType.PROCEDURE.value,
            nesting_level=curr_nesting_level+1
        )
        
        procedure_symbol = node.procedure_symbol
        params = procedure_symbol.params
        actual_params = node.actual_params
        
        for param, actual_param in zip(params, actual_params):
            record[param.name] = self.visit_node(actual_param)
            
        print(f"Enter PROCEDURE {procedure_name}")
        self.call_stack.push(record)
        self.visit_node(procedure_symbol.block)
        print(str(self.call_stack))
        self.call_stack.pop()
        print(f"Leave PROCEDURE {procedure_name}")


    def visit_assignment_statement(self, node):
        variable_name = node.left_node.value
        variable_value = self.visit_node(node.right_node)
    
        curr_record = self.call_stack.peek()
        curr_record[variable_name] = variable_value

    
    def visit_case_statement(self, node):
        pass
    
    
    def visit_case_compound(self, node):
        pass
    
    
    def visit_default_compound(self, node):
        pass


    def visit_comparison(self, node):
        left_part = self.visit_node(node.left_node)
        right_part = self.visit_node(node.right_node)
    
    
    def visit_input_statement(self, node):
        pass
    
    
    def visit_output_statement(self, node):
        pass
    
    
    def visit_if_statement(self, node):
        pass
    
    
    def visit_for_statement(self, node):
        pass
    
    
    def visit_while_statement(self, node):
        pass
    
    
    def visit_repeat_statement(self, node):
        pass


    def visit_variable(self, node):
        variable_name = node.value
        curr_record = self.call_stack.peek()
        
        variable_value = curr_record.get(variable_name)
        return variable_value
        
        
    def visit_literal(self, node):
        return node.value
    
    
    def visit_number(self, node):
        return node.value
    
    
    def visit_logical_operation(self, node):
        match(node.operation.value):
            case TOKEN_TYPES.OR.value:
                return self.visit_node(node.left_node) or self.visit_node(node.right_node)
            
            case TOKEN_TYPES.AND.value:
                return self.visit_node(node.left_node) and self.visit_node(node.right_node)
            
            case TOKEN_TYPES.XOR.value:
                return xor(self.visit_node(node.left_node), self.visit_node(node.right_node))


    def visit_binary_operation(self, node):
        match(node.operation.type):
            case TOKEN_TYPES.PLUS.value:
                return self.visit_node(node.left_node) + self.visit_node(node.right_node)
            
            case TOKEN_TYPES.MINUS.value:
                return self.visit_node(node.left_node) - self.visit_node(node.right_node)
            
            case TOKEN_TYPES.MUL.value:
                return self.visit_node(node.left_node) * self.visit_node(node.right_node)
            
            case TOKEN_TYPES.INTEGER_DIV.value:
                return int(self.visit_node(node.left_node) / self.visit_node(node.right_node))
            
            case TOKEN_TYPES.FLOAT_DIV:
                return self.visit_node(node.left_node) / self.visit_node(node.right_node)


    def visit_unary_operation(self, node):
        if node.operation.type == TOKEN_TYPES.PLUS: return +self.visit_node(node.expr)
        else: return -self.visit_node(node.expr)
        
        
    def visit_jump_statement(self, node):
        pass
    
    
    def visit_empty_operation(self, node):
        pass
    
    
    def visit_type_dec(self, node):
        pass


    def evaluate(self):
        self.start_visit()

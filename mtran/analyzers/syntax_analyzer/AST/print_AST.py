from .visitor_AST import AST_Visitor

class AST_Printer(AST_Visitor):

    def __init__(self, ast_tree):
        super().__init__(ast_tree)
        self.ignore = False 


    def visit_program(self, node):
        self.print_message(f"Program {node.name}")
        self.visit_node(node.block)


    def visit_block(self, node):
        self.print_message(f"Block:")
        self.visit_node(node.declaration)
        self.visit_node(node.compound_statement)


    def visit_declaration(self, node):
        self.print_message(f"Declaration:")

        for declaration in node.declaration_list:
            self.visit_node(declaration)


    def visit_variable_declaration(self, node):
        self.print_message(f"Var declaration:")
        self.visit_node(node.variable_node)
        self.visit_node(node.type_node)


    def visit_procedure_declaration(self, node):
        self.print_message(f"Procedure {node.name.value}")
        self.visit_node(node.block_node)


    def visit_type_dec(self, node):
        self.print_message(f"Type: {node.value}")


    def visit_compound_statement(self, node):
        self.print_message(f"Compound:")
        
        for statement in node.statement_list:
            self.visit_node(statement)


    def visit_assignment_statement(self, node):
        self.print_message(f"Assignment:")
        self.visit_node(node.left_node)
        self.print_message(f"'{node.operation.value}'")
        self.visit_node(node.right_node)
        
        
    def visit_jump_statement(self, node):
        self.print_message(f"'{node.jump}'")
        
        if node.expr != None:
            self.visit_node(node.expr)
        
        
    def visit_case_statement(self, node):
        self.print_message(f"Case:")
        self.visit_node(node.condition)
        
        for case in node.case_list:
            self.visit_node(case)
        
        
    def visit_case_compound(self, node):
        self.visit_node(node.case)
        self.print_message(f"':'")
        self.visit_node(node.result)
    
    
    def visit_default_compound(self, node):
        self.print_message(f"{node.default}")
        self.visit_node(node.result)


    def visit_comparison(self, node):
        self.print_message(f"Comparison:")
        self.visit_node(node.left_node)
        self.print_message(f"'{node.operation.value}'")
        self.visit_node(node.right_node)


    def visit_input_statement(self, node):
        self.print_message(f"Readln:")

        for input in node.input_list:
            self.visit_node(input)


    def visit_output_statement(self, node):
        self.print_message(f"Writeln:")

        for output in node.output_list:
            self.visit_node(output)


    def visit_if_statement(self, node):
        self.print_message(f"If:")
        self.visit_node(node.comparison)
        self.visit_node(node.statement)

        if node.next_statement != None:
            self.print_message(f"Else:")
            self.visit_node(node.next_statement)
            
            
    def visit_for_statement(self, node):
        self.print_message(f"Loop For:")
        self.visit_node(node.assignment[0])
        self.print_message(f"To:")
        self.visit_node(node.border[0])
        self.print_message(f"Do:")
        self.visit_node(node.statement)
    
    
    def visit_while_statement(self, node):
        self.print_message(f"Loop While:")
        self.visit_node(node.border)
        self.print_message("Do")
        self.visit_node(node.statement)
    
    
    def visit_repeat_statement(self, node):
        self.print_message(f"Loop Repeat:")
        self.visit_node(node.statement[0])
        self.print_message("Until")
        self.visit_node(node.border)


    def visit_variable(self, node):
        self.print_message(f"Variable: '{node.value}'")


    def visit_literal(self, node):
        self.print_message(f"Literal: '{node.value}'")


    def visit_number(self, node):
        self.print_message(f"Number: '{node.value}'")


    def visit_empty_operation(self, node):
        self.print_message(f"EmptyOperation")


    def visit_logical_operation(self, node):
        self.print_message(f"LogicalOperation:")
        self.visit_node(node.left_node)
        self.print_message(f"'{node.operation.value}'")
        self.visit_node(node.right_node)
    
    
    def visit_binary_operation(self, node):
        self.print_message(f"BinaryOperation:")
        self.visit_node(node.left_node)
        self.print_message(f"'{node.operation.value}'")
        self.visit_node(node.right_node)


    def visit_unary_operation(self, node):
        self.print_message(f"UnaryOperation: '{node.operation.value}'")
        self.visit_node(node.expr)


    def print_message(self, message):
        if self.ignore:
            return
        
        offset = " | " * self.depth if self.depth else ""
        print(f"{offset}{message}")


    def print_ast(self, ignore=False):
        self.ignore = ignore
        self.start_visit()
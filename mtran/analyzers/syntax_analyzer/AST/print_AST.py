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


    def visit_comparison_statement(self, node):
        pass


    def visit_change_statement(self, node):
        pass


    def visit_variable(self, node):
        self.print_message(f"Variable: '{node.value}'")


    def visit_literal(self, node):
        self.print_message(f"Literal: '{node.value}'")


    def visit_number(self, node):
        self.print_message(f"Number: '{node.value}'")


    def visit_empty_operation(self, node):
        self.print_message(f"EmptyOperation")


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
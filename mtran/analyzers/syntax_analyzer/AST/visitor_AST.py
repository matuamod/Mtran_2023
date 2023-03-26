from abc import ABC, abstractmethod
from .AST import *

class AST_Visitor(ABC):

    def __init__(self, ast_tree):

        self.nodes_handler = {
            Program : self.visit_program,
            Block : self.visit_block,
            Declaration : self.visit_declaration,
            VariableDeclaration : self.visit_variable_declaration,
            ProcedureDeclaration : self.visit_procedure_declaration,
            Type : self.visit_type_dec,
            CompoundStatement : self.visit_compound_statement,
            AssignmentStatement : self.visit_assignment_statement,
            ComparisonStatement : self.visit_comparison_statement,
            InputStatement : self.visit_input_statement,
            OutputStatement : self.visit_output_statement,
            Variable : self.visit_variable,
            Literal : self.visit_literal,
            Number : self.visit_number,
            EmptyOperation : self.visit_empty_operation,
            BinaryOperation : self.visit_binary_operation,
            UnaryOperation : self.visit_unary_operation
        }
        self.ast_tree = ast_tree
        self.path = list()
        self.depth = 0


    @abstractmethod
    def visit_program(self, node):
        pass


    @abstractmethod
    def visit_block(self, node):
        pass


    @abstractmethod
    def visit_declaration(self, node):
        pass


    @abstractmethod
    def visit_variable_declaration(self, node):
        pass


    @abstractmethod
    def visit_procedure_declaration(self, node):
        pass


    @abstractmethod
    def visit_type_dec(self, node):
        pass


    @abstractmethod
    def visit_compound_statement(self, node):
        pass


    @abstractmethod
    def visit_assignment_statement(self, node):
        pass


    @abstractmethod
    def visit_comparison_statement(self, node):
        pass


    @abstractmethod
    def visit_input_statement(self, node):
        pass


    @abstractmethod
    def visit_output_statement(self, node):
        pass


    @abstractmethod
    def visit_variable(self, node):
        pass


    @abstractmethod
    def visit_literal(self, node):
        pass


    @abstractmethod
    def visit_number(self, node):
        pass


    @abstractmethod
    def visit_empty_operation(self, node):
        pass


    @abstractmethod
    def visit_binary_operation(self, node):
        pass


    @abstractmethod
    def visit_unary_operation(self, node):
        pass


    def visit_node(self, node):
        if not node:
            return
        
        self.path.append(node)

        self.depth += 1
        result = self.nodes_handler[type(node)](node)
        self.depth -= 1

        return result


    def start_visit(self):
        self.path.clear()
        self.visit_node(self.ast_tree)


    
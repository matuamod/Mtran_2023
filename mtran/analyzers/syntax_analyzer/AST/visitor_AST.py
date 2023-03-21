from abc import ABC, abstractmethod
from .AST import *

class AST_Visitor(ABC):

    def __init__(self, ast_tree):

        self.nodes_handler = {
            CompoundStatement : self.visit_compound_statement,
            AssignmentStatement : self.visit_assignment_statement,
            Variable : self.visit_variable,
            Number : self.visit_number,
            EmptyOperation : self.visit_empty_operation,
            BinaryOperation : self.visit_binary_operation,
            UnaryOperation : self.visit_unary_operation
        }
        self.ast_tree = ast_tree
        self.path = list()
        self.depth = 0


    @abstractmethod
    def visit_compound_statement(self, node):
        pass


    @abstractmethod
    def visit_assignment_statement(self, node):
        pass


    @abstractmethod
    def visit_variable(self, node):
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


    
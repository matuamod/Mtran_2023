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
            FunctionDeclaration : self.visit_function_declaration,
            Type : self.visit_type_dec,
            CompoundStatement : self.visit_compound_statement,
            CallStatement : self.visit_call,
            AssignmentStatement : self.visit_assignment_statement,
            JumpStatement : self.visit_jump_statement,
            CaseStatement : self.visit_case_statement,
            CaseCompound : self.visit_case_compound,
            DefaultCompound : self.visit_default_compound,
            ComparisonStatement : self.visit_comparison,
            InputStatement : self.visit_input_statement,
            OutputStatement : self.visit_output_statement,
            IfStatement : self.visit_if_statement,
            ForLoop : self.visit_for_statement,
            WhileLoop : self.visit_while_statement,
            RepeatLoop : self.visit_repeat_statement,
            Variable : self.visit_variable,
            Literal : self.visit_literal,
            Number : self.visit_number,
            EmptyOperation : self.visit_empty_operation,
            LogicalOperation : self.visit_logical_operation,
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
    def visit_function_declaration(self, node):
        pass


    @abstractmethod
    def visit_type_dec(self, node):
        pass


    @abstractmethod
    def visit_compound_statement(self, node):
        pass
    
    
    @abstractmethod
    def visit_call(self, node):
        pass


    @abstractmethod
    def visit_case_compound(self, node):
        pass
    
    
    @abstractmethod
    def visit_default_compound(self, node):
        pass


    @abstractmethod
    def visit_assignment_statement(self, node):
        pass


    @abstractmethod
    def visit_jump_statement(self, node):
        pass


    @abstractmethod
    def visit_case_statement(self, node):
        pass


    @abstractmethod
    def visit_comparison(self, node):
        pass


    @abstractmethod
    def visit_input_statement(self, node):
        pass


    @abstractmethod
    def visit_output_statement(self, node):
        pass


    @abstractmethod
    def visit_if_statement(self, node):
        pass
    
    
    @abstractmethod
    def visit_for_statement(self, node):
        pass
    
    
    @abstractmethod
    def visit_while_statement(self, node):
        pass
    
    
    @abstractmethod
    def visit_repeat_statement(self, node):
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
    def visit_logical_operation(self, node):
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


    

class AST(object):
   pass


class Program(AST):

    def __init__(self, name, block):
        self.name = name
        self.block = block


class Block(AST):

    def __init__(self, declaration, compound_statement):
        self.declaration = declaration
        self.compound_statement = compound_statement


class Declaration(AST):

    def __init__(self):
        self.declaration_list = list()


class VariableDeclaration(AST):

    def __init__(self, variable_node, type_node):
        self.variable_node = variable_node
        self.type_node = type_node


class ProcedureDeclaration(AST):

    def __init__(self, name, params, block):
        self.name = name
        self.params = params
        self.block_node = block
        

class ProcedureParams(AST):
    
    def __init__(self, variable_node, type_node):
        self.variable_node = variable_node
        self.type_node = type_node
        
        
class ProcedureCall(AST):
    
    def __init__(self, procedure_name, actual_params, token):
        self.procedure_name = procedure_name
        self.actual_params = actual_params 
        self.token = token
        self.procedure_symbol = None


class Type(AST):

    def __init__(self, token):
        self.token = token
        self.value = token.value


class CompoundStatement(AST):

    def __init__(self):
        self.statement_list = list()


class AssignmentStatement(AST):
    
    def __init__(self, left_node, token, right_node):
        self.left_node = left_node
        self.token = token
        self.operation = token
        self.right_node = right_node
        
        
class JumpStatement(AST):
    
    def __init__(self, jump, expr=None):
        self.jump = jump
        self.expr = expr


class ForLoop(AST):
    
    def __init__(self, assignment, border, statement):
        self.assignment = assignment,
        self.border = border,
        self.statement = statement
        
        
class WhileLoop(AST):
    
    def __init__(self, border, statement):
        self.border = border
        self.statement = statement
        
        
class RepeatLoop(AST):
    
    def __init__(self, statement, border):
        self.statement = statement,
        self.border = border


class CaseStatement(AST):

    def __init__(self, condition, case_list):
        self.condition = condition
        self.case_list = case_list
        
        
class CaseCompound(AST):
    
    def __init__(self, case, result):
        self.case = case
        self.result = result
        
        
class DefaultCompound(AST):
    
    def __init__(self, default, result):
        self.default = default
        self.result = result


class ComparisonStatement(AST):
     
     def __init__(self, left_node, token, right_node):
        self.left_node = left_node
        self.token = token
        self.operation = token
        self.right_node = right_node


class InputStatement(AST):
    
    def __init__(self):
        self.input_list = list()


class OutputStatement(AST):
    
    def __init__(self):
        self.output_list = list()


class IfStatement(AST):

    def __init__(self, comparison, statement, next_statement=None):
        self.comparison = comparison
        self.statement = statement
        self.next_statement = next_statement


class Variable(AST):
    
    def __init__(self, token):
        self.token = token
        self.value = token.value
        self.variable_type = None


class Literal(AST):

    def __init__(self, token):
        self.token = token
        self.value = token.value


class Number(AST):

    def __init__(self, token):
        self.token = token
        self.value = token.value


class EmptyOperation(AST):
    pass


class LogicalOperation(AST):
    
    def __init__(self, left_node, token, right_node):
        self.left_node = left_node
        self.token = token
        self.operation = token
        self.right_node = right_node


class BinaryOperation(AST):
    
    def __init__(self, left_node, token, right_node):
        self.left_node = left_node
        self.token = token
        self.operation = token
        self.right_node = right_node


class UnaryOperation(AST):

    def __init__(self, token, expr):
        self.token = token
        self.operation = token
        self.expr = expr
    
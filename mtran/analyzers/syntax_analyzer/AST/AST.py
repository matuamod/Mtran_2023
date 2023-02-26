
class AST(object):
   pass


class CompoundStatement(AST):

    def __init__(self):
        self.statement_list = list()


class AssignmentStatement(AST):
    
    def __init__(self, left_node, token, right_node):
        self.left_node = left_node
        self.token = token
        self.right_node = right_node


class Variable(AST):
    
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Number(AST):

    def __init__(self, token):
        self.token = token
        self.value = token.value


class EmptyOperation(AST):
    pass


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
    
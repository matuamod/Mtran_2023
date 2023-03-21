from analyzers import TOKEN_TYPES
from .node_visitor import NodeVisitor

class Interpreter(NodeVisitor):

    def __init__(self, syntax_analyzer):
        self.syntax_analyzer = syntax_analyzer
        self.GLOBAL_SCOPE = dict()


    def visit_CompoundStatement(self, node):

        for statement in node.statement_list:
            self.visit(statement)


    def visit_AssignmentStatement(self, node):
        variable_name = node.left_node.value
        self.GLOBAL_SCOPE[variable_name] = self.visit(node.right_node)


    def visit_Variable(self, node):
        variable_name = node.value
        value = self.GLOBAL_SCOPE.get(variable_name)

        if value is not None:
            return value
        else:
            raise NameError(repr(variable_name))


    def visit_BinaryOperation(self, node):

        if node.operation.type == TOKEN_TYPES.PLUS:
            return self.visit(node.left_node) + self.visit(node.right_node)
        elif node.operation.type == TOKEN_TYPES.MINUS:
            return self.visit(node.left_node) - self.visit(node.right_node)
        elif node.operation.type == TOKEN_TYPES.MUL:
            return self.visit(node.left_node) * self.visit(node.right_node)
        elif node.operation.type == TOKEN_TYPES.INTEGER_DIV:
            return int(self.visit(node.left_node) / self.visit(node.right_node))
        elif node.operation.type == TOKEN_TYPES.FLOAT_DIV:
            return self.visit(node.left_node) / self.visit(node.right_node)


    def visit_UnaryOperation(self, node):
        # print(node.operation.type)

        if node.operation.type == TOKEN_TYPES.PLUS:
            return +self.visit(node.expr)
        elif node.operation.type == TOKEN_TYPES.MINUS:
            return -self.visit(node.expr)


    def visit_Number(self, node):
        return node.value


    def visit_EmptyOperation(self, node):
        pass


    def evaluate(self):
        # By using makeParse() method we can get Abstract Syntax Tree 
        tree = self.syntax_analyzer.make_parse()
        return self.visit(tree)

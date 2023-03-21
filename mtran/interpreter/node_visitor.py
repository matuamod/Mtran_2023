
class NodeVisitor(object):

    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.checkForVisit)
        return visitor(node)


    def checkForVisit(self, node):
        raise Exception('No visit{} method'.format(type(node).__name__))
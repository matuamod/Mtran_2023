import os
from analyzers import LexicalAnalyzer, SyntaxAnalyzer, LexicalError, AST_Printer
from interpreter import Interpreter

def main():
    filepath = "tests/test2.pas"
    
    with open(filepath, 'r') as f:
        code_lines = f.readlines()
        code = ''.join(code_lines)

    try:
        code = get_code(filepath)

        try:
            lexical_analyzer = LexicalAnalyzer(code)
            syntax_analyzer = SyntaxAnalyzer(lexical_analyzer)
            ast_tree = syntax_analyzer.make_parse()

            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            ast_printer = AST_Printer(ast_tree)
            ast_printer.print_ast()

            # interpreter = Interpreter(syntax_analyzer)
            # result = interpreter.evaluate()
            # print(result)
            # print(interpreter.GLOBAL_SCOPE)
        except LexicalError as e:
            code_line = code_lines[e.line_num-1][:-1]
            print(code_line)
            print('~^~'.rjust(e.column_num+1))
            print(e)
        
    except EOFError:
        exit()


def get_code(filepath):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), filepath))

    with open(path, "r") as f:
        code = f.read()

    return code


def add_new_row(table, column_name, token, variable_type):
    for row in table:
        row.border = False
        row.header = False

        if row.get_string(fields=[column_name]).strip() == token.value:
            return

    table.add_row([token.value, variable_type])


if __name__ == "__main__":
    main()

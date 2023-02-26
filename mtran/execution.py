import os
from analyzers import LexicalAnalyzer, SyntaxAnalyzer, LexicalError, ErrorTypes
from interpreter import Interpreter

def main():
    filepath = "tests/test2.pas"
    code = getCode(filepath)

    lexical_analyzer = LexicalAnalyzer(code)

    with open(filepath, 'r') as f:
        code_lines = f.readlines()
        code = ''.join(code_lines)
        print(code)

    while True:
        try:
            token = lexical_analyzer.getNextToken()
            print(token)
            if token.value == None:
                break
        except LexicalError as e:
            print()
            code_line = code_lines[e.line_num-1][:-1]
            print(code_line)
            print('~^~'.rjust(e.column_num+1))
            print(e)
            break

    
#     while True:
#         try:
#             # text = input("matuamod> ")
#             text = """\
#         except EOFError:
#             break
#         if not text:
#             continue
#         elif text == "exit":
#             print("Successfully exit")
#             return
#         lexical_analyzer = LexicalAnalyzer(text)
#         syntax_analyzer = SyntaxAnalyzer(lexical_analyzer)
#         interpreter = Interpreter(syntax_analyzer)
#         result = interpreter.evaluate()
#         print(result)
#         print(interpreter.GLOBAL_SCOPE)
#         time.sleep(10)


def getCode(filepath):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), filepath))

    with open(path, "r") as f:
        # code_lines = f.readlines()
        code = f.read()

    return code


if __name__ == "__main__":
    main()


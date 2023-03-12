import os
from analyzers import LexicalAnalyzer, SyntaxAnalyzer, LexicalError, ErrorTypes, TOKEN_TYPES, RESERVED_TOKENS
from interpreter import Interpreter
from prettytable import PrettyTable
import re


def main():
    filepath = "tests/test2.pas"
    code = get_code(filepath)
    variables_table = PrettyTable(["Variable value", "Variable type"])
    key_words_table = PrettyTable(["Key Word value", "Key Word type"])
    constants_table = PrettyTable(["Constants value", "Constants type"])
    operators_table = PrettyTable(["Operator value", "Operator type"])

    lexical_analyzer = LexicalAnalyzer(code)

    with open(filepath, 'r') as f:
        code_lines = f.readlines()
        code = ''.join(code_lines)

    while True:
        try:
            token = lexical_analyzer.getNextToken()

            if token.type == TOKEN_TYPES.ID.value:
                variable_type = f'variable of {token.type}, ' + \
                    'type after syntax analyzer'
                add_new_row(variables_table, "Variable value",
                            token, variable_type)
            elif token.type in RESERVED_TOKENS.keys():
                key_word_type = f"key word of '{token.type}'"
                add_new_row(key_words_table, "Key Word value",
                            token, key_word_type)
            elif str(token.type).endswith("_CONST"):
                constant_type = f"'{token.type.rstrip('_CONST')}' constant"
                add_new_row(constants_table, "Constants value",
                            token, constant_type)
            elif token.type not in RESERVED_TOKENS.keys() and \
                    token.type != TOKEN_TYPES.EOF.value:
                if re.match(r'(\d+)|[-+*/]', str(token.value)):
                    arithmetic_type = "is arithmetic operator"
                    add_new_row(operators_table, "Operator value",
                                token, arithmetic_type)
                elif re.match(r'(\d+)|[=<>]', str(token.value)):
                    comparison_type = "is comparison operator/renational operator"
                    add_new_row(operators_table, "Operator value",
                                token, comparison_type)
                else:
                    default_type = f"is {token.type.lower()} operator"
                    add_new_row(operators_table, "Operator value",
                                token, default_type)

            if token.value == None:
                print(variables_table)
                print(key_words_table)
                print(constants_table)
                print(operators_table)
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

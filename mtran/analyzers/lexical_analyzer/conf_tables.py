from .tokens import TOKEN_TYPES
from .tokens import RESERVED_TOKENS
from prettytable import PrettyTable
import re

class ConfigureTables(object):

    def __init__(self):
        self.variables_table = PrettyTable(["Variable value", "Variable type"])
        self.key_words_table = PrettyTable(["Key Word value", "Key Word type"])
        self.constants_table = PrettyTable(["Constants value", "Constants type"])
        self.operators_table = PrettyTable(["Operator value", "Operator type"])


    def fill_table(self, token):
        if token.type == TOKEN_TYPES.ID.value:
            variable_type = f'variable of {token.type}, ' + \
                'type after syntax analyzer'
            self.variables_table.add_row([token.value, variable_type])
        elif token.type in RESERVED_TOKENS.keys():
            key_word_type = f"key word of '{token.type}'"
            self.key_words_table.add_row([token.value, key_word_type])
        elif str(token.type).endswith("_CONST"):
            constant_type = f"'{token.type.rstrip('_CONST')}' constant"
            self.constants_table.add_row([token.value, constant_type])
        elif token.type not in RESERVED_TOKENS.keys() and \
                token.type != TOKEN_TYPES.EOF.value:
            if re.match(r'(\d+)|[-+*/]', str(token.value)):
                arithmetic_type = "is arithmetic operator"
                self.operators_table.add_row([token.value, arithmetic_type])
            elif re.match(r'(\d+)|[=<>]', str(token.value)):
                comparison_type = "is comparison operator/renational operator"
                self.operators_table.add_row([token.value, comparison_type])
            else:
                default_type = f"is {token.type.lower()} operator"
                self.operators_table.add_row([token.value, default_type])

        if token.value == None:
            self.print_table()
                

    def print_table(self):
        print(self.variables_table)
        print(self.key_words_table)
        print(self.constants_table)
        print(self.operators_table)

            

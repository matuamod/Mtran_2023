from operator import xor
from analyzers import TOKEN_TYPES
from analyzers.syntax_analyzer import AST_Visitor
from .stack import CallStack, Record, RecordType
import time

class Interpreter(AST_Visitor):

    def __init__(self, ast_tree):
        super().__init__(ast_tree)
        self.ast_tree = ast_tree
        self.call_stack = CallStack()
        
        
    def visit_program(self, node):
        program_name = node.name
        print(f"Enter PROGRAM {program_name}")
        
        record = Record(
            name=program_name,
            type=RecordType.PROGRAM.value,
            nesting_level=1
        )
        
        self.call_stack.push(record)
        self.visit_node(node.block)
        self.call_stack.pop()
        print(f"Leave PROGRAM {program_name}")
    
    
    def visit_block(self, node):
        self.visit_node(node.declaration)
        self.visit_node(node.compound_statement)
    
    
    def visit_declaration(self, node):
        for declaration in node.declaration_list:
            self.visit_node(declaration)
    
    
    def visit_variable_declaration(self, node):
        self.visit_node(node.variable_node)
        self.visit_node(node.type_node)
    

    def visit_compound_statement(self, node):
        for statement in node.statement_list:
            self.visit_node(statement)
            
            
    def visit_call(self, node):
        call_name = node.name.value
        curr_nesting_level = self.call_stack.peek().nesting_level
        symbol = node.symbol
        
        if symbol.__class__.__name__ == "FunctionSymbol":    
            record = Record(
                name=call_name,
                type=RecordType.FUNCTION.value,
                nesting_level=curr_nesting_level+1
            )
        elif symbol.__class__.__name__ == "ProcedureSymbol":
            record = Record(
                name=call_name,
                type=RecordType.PROCEDURE.value,
                nesting_level=curr_nesting_level+1
            )
        
        params = symbol.params
        actual_params = node.actual_params
        
        for param, actual_param in zip(params, actual_params):
            record[param.name] = self.visit_node(actual_param)
            
        # print(f"Enter {symbol.__class__.__name__} {call_name}")
        self.call_stack.push(record)
        self.visit_node(symbol.block)
        # print(str(self.call_stack))
        
        if symbol.__class__.__name__ == "FunctionSymbol":
            ret_value = self.call_stack.peek().get(call_name)
            self.call_stack.pop()
            # print(f"Call result: {ret_value}")
            # print(f"Leave {symbol.__class__.__name__} {call_name}")
            return ret_value
        
        self.call_stack.pop()
        # print(f"Leave {symbol.__class__.__name__} {call_name}")


    def visit_assignment_statement(self, node):
        variable_name = node.left_node.value
        variable_value = self.visit_node(node.right_node)
    
        curr_record = self.call_stack.peek()
        
        if node.operation.type == TOKEN_TYPES.ASSINGMENT.value:
            curr_record[variable_name] = variable_value
        else:
            curr_value = curr_record.get(variable_name)
            
            if curr_value == None: 
                curr_record[variable_name] = 0
                curr_value = curr_record.get(variable_name)
                
            curr_value += variable_value

    
    def visit_case_statement(self, node):
        condition = self.visit_node(node.condition)
        
        for case in node.case_list:
            case_value, result = self.visit_node(case)

            if case_value == condition:
                self.visit_node(result)
                return
            elif case_value == "Else":
                self.visit_node(result)
    
    
    def visit_case_compound(self, node):
        case_value = self.visit_node(node.case)
        result = node.result
        return case_value, result
    
    
    def visit_default_compound(self, node):
        default = node.default
        result = node.result
        return default, result


    def visit_comparison(self, node): 
        left_side = self.visit_node(node.left_node)
        right_side = self.visit_node(node.right_node)
        
        match(node.operation.type):
            case TOKEN_TYPES.EQUAL.value:
                return True if left_side == right_side else False
            
            case TOKEN_TYPES.NONEQUAL.value:
                return True if left_side != right_side else False
            
            case TOKEN_TYPES.GREATER.value:
                return True if left_side > right_side else False
            
            case TOKEN_TYPES.LESS.value:
                return True if left_side < right_side else False
            
            case TOKEN_TYPES.GREATER_OR_EQUAL.value:
                return True if left_side >= right_side else False
            
            case TOKEN_TYPES.LESS_OR_EQUAL.value:
                return True if left_side <= right_side else False
    
    
    def visit_input_statement(self, node):
        curr_record = self.call_stack.peek()
        
        for input_var in node.input_list:
            input_value = input(f"Input {input_var.value}: ")
            
            match(input_var.token.type):
                case TOKEN_TYPES.INTEGER.value:
                    curr_record[input_var.value] = int(input_value)
                    
                case TOKEN_TYPES.REAL.value:
                    curr_record[input_var.value] = float(input_value)
                    
                case _:
                    curr_record[input_var.value] = str(input_value)
    
    
    def visit_output_statement(self, node):        
        for output in node.output_list:
            print(f"Output: {self.visit_node(output)}")
    
    
    def visit_if_statement(self, node):
        comparison = self.visit_node(node.comparison)
        
        if comparison:
            self.visit_node(node.statement)
            return
        if node.next_statement != None:
            self.visit_node(node.next_statement)
    
    
    def visit_for_statement(self, node):
        assignment_value = self.visit_node(node.assignment[0].right_node)
        border_value = self.visit_node(node.border[0])
        
        if assignment_value < border_value:
            
            while assignment_value < border_value:
                self.visit_node(node.statement)
                assignment_value += 1
    
    
    def visit_while_statement(self, node):
        while self.visit_node(node.border):
            
            if node.border.__class__.__name__ == "ComparisonStatement":
                if node.border.left_node.__class__.__name__ == "Variable":
                    curr_record = self.call_stack.peek()
                    left_side = curr_record.get(node.border.left_node.value)
                    left_side += 1
                    curr_record[node.border.left_node.value] = left_side
    
            self.visit_node(node.statement)
    
    
    def visit_repeat_statement(self, node):
        self.visit_node(node.statement[0])
        
        while self.visit_node(node.border):
            
            if node.border.__class__.__name__ == "ComparisonStatement":
                if node.border.left_node.__class__.__name__ == "Variable":
                    curr_record = self.call_stack.peek()
                    left_side = curr_record.get(node.border.left_node.value)
                    left_side += 1
                    curr_record[node.border.left_node.value] = left_side
    
            self.visit_node(node.statement[0])


    def visit_variable(self, node):
        variable_name = node.value
        curr_record = self.call_stack.peek()
        variable_value = curr_record.get(variable_name)
        
        if variable_value == None:   
                     
            if node.variable_type in (
                TOKEN_TYPES.INTEGER.value,
                TOKEN_TYPES.REAL.value
            ): return 0
            else: return str()
            
        return variable_value
        
        
    def visit_literal(self, node):
        if node.value == "TRUE": return True
        elif node.value == "FALSE": return False
        else: return node.value
    
    
    def visit_number(self, node):
        return node.value
    
    
    def visit_logical_operation(self, node):
        match(node.operation.value):
            case TOKEN_TYPES.OR.value:
                return self.visit_node(node.left_node) or self.visit_node(node.right_node)
            
            case TOKEN_TYPES.AND.value:
                return self.visit_node(node.left_node) and self.visit_node(node.right_node)
            
            case TOKEN_TYPES.XOR.value:
                return xor(self.visit_node(node.left_node), self.visit_node(node.right_node))


    def visit_binary_operation(self, node):
        match(node.operation.type):
            case TOKEN_TYPES.PLUS.value:
                return self.visit_node(node.left_node) + self.visit_node(node.right_node)
            
            case TOKEN_TYPES.MINUS.value:
                return self.visit_node(node.left_node) - self.visit_node(node.right_node)
            
            case TOKEN_TYPES.MUL.value:
                return self.visit_node(node.left_node) * self.visit_node(node.right_node)
            
            case TOKEN_TYPES.INTEGER_DIV.value:
                return int(self.visit_node(node.left_node) / self.visit_node(node.right_node))
            
            case TOKEN_TYPES.FLOAT_DIV:
                return self.visit_node(node.left_node) / self.visit_node(node.right_node)


    def visit_unary_operation(self, node):
        if node.operation.type == TOKEN_TYPES.PLUS: return +self.visit_node(node.expr)
        else: return -self.visit_node(node.expr)
        
        
    def visit_function_declaration(self, node):
        pass
    
    
    def visit_procedure_declaration(self, node):
        pass
    
    
    def visit_jump_statement(self, node):
        pass
    
    
    def visit_empty_operation(self, node):
        pass
    
    
    def visit_type_dec(self, node):
        pass


    def evaluate(self):
        self.start_visit()

from .symbols import BuiltinTypeSymbol

class ScopedSymbolTable(object):
    
    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        # Symbols dict in current scope
        self.symbols_dict = dict()
        # Name of the current scope
        self.scope_name = scope_name
        # Level of the current scope
        self.scope_level = scope_level
        # Link for scope which has higher area elected level
        self.enclosing_scope = enclosing_scope

        
    def __str__(self):
        scope_table_header = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', scope_table_header, '=' * len(scope_table_header)]
        for header_name, header_value in (
            ('Scope name', self.scope_name),
            ('Scope level', self.scope_level),
            ('Enclosing scope',
             self.enclosing_scope.scope_name if self.enclosing_scope else None
            )
        ):
            lines.append('%-15s: %s' % (header_name, header_value))
        table_header = "Scope (Scoped symbol table) contents"
        lines.extend(["\n", table_header, "-" * len(table_header)])
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self.symbols_dict.items()
        )
        lines.append("\n")
        
        result = "\n".join(lines)
        return result
    
    
    __repr__ = __str__   
    
    
    def insert(self, symbol):
        print(f"Insert: {symbol.name}")
        self.symbols_dict[symbol.name] = symbol
        
        
    def lookup(self, name, current_scope_only=False):
        print(f"Lookup: {name}")
        symbol = self.symbols_dict.get(name)
        
        if symbol is not None:
            return symbol
        
        if current_scope_only:
            return None
        
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)
        
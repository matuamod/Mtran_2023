from .symbols import BuiltinTypeSymbol

class SymbolTable(object):
    
    def __init__(self):
        self.symbols_dict = dict()

        
    def __str__(self):
        table_header = "Symbol table contents"
        lines = ["\n", table_header, "_" * len(table_header)]
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self.symbols_dict.items()
        )
        lines.append("\n")
        
        result = "\n".join(lines)
        return result
    
    
    __repr__ = __str__   
    
    
    def insert(self, symbol):
        # print(f"Insert: {symbol.name}")
        self.symbols_dict[symbol.name] = symbol
        
        
    def lookup(self, name):
        # print(f"Lookup: {name}")
        symbol = self.symbols_dict.get(name)
        return symbol
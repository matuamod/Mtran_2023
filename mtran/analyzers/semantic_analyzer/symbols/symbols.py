
class Symbol(object):
    
    def __init__(self, name, type=None):
        self.name = name
        self.type = type
        
        
class BuiltinTypeSymbol(Symbol):
    
    def __init__(self, name):
        super().__init__(name)
            
    def __str__(self):
        return "<{class_name}(name='{name}')>".format(
            class_name=self.__class__.__name__,
            name=self.name
        )
    
    __repr__ = __str__
        
        
class VariableSymbol(Symbol):
    
    def __init__(self, name, type):
        super().__init__(name, type)
        
    def __str__(self):
        return "<{class_name}(name='{name}', type='{type}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
            type=self.type.name
        )
        
    __repr__ = __str__
    
    
class ProcedureSymbol(Symbol):
    
    def __init__(self, name, params=None):
        super().__init__(name)
        self.params = params if params is not None else list()
        self.block = None
        
    def __str__(self):
        return "<{class_name}(name='{name}', parameters='{params}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
            params=self.params
        )

    __repr__ = __str__
    
    
class FunctionSymbol(Symbol):
    
    def __init__(self, name, ret_type, params=None):
        super().__init__(name)
        self.ret_type = ret_type
        self.params = params if params is not None else list()
        self.block = None
        
    def __str__(self):
        return "<{class_name}(name='{name}', return type='{ret_type}' parameters='{params}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
            ret_type=self.ret_type,
            params=self.params
        )

    __repr__ = __str__
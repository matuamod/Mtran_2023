
class CallStack(object):
    
    def __init__(self):
        self._records = list()
        
    def push(self, record):
        self._records.append(record)
        
    def pop(self):
        return self._records.pop()
    
    def peek(self):
        return self._records[-1]
    
    def __str__(self):
        stack = "\n".join(str(record) for record in self._records)
        stack_repr = f"Call stack\n{stack}"
        return stack_repr
    
    def __repr__(self):
        return self.__str__()
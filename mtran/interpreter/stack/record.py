
class Record(object):
    
    def __init__(self, name, type, nesting_level):
        self.name = name
        self.type = type
        self.nesting_level = nesting_level
        self._record_data = dict()
        

    def __setitem__(self, key, value):
        self._record_data[key] = value
        
        
    def __getitem__(self, key):
        return self._record_data[key]
    
    
    def get(self, key):
        return self._record_data.get(key)
    
    
    def __str__(self):
        records = [f"Record: Type: '{self.type}' Name: '{self.name}' Nesting level: '{self.nesting_level}'"]
        
        for key, value in self._record_data.items():
            records.append(f"{key:<20}: '{value}'")
            
        return "\n".join(records)
        
        
    def __repr__(self):
        return self.__str__()
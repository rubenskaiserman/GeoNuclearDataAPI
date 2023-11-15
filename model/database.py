import pandas as pd

class Client:
    def __init__(self):
        df = pd.read_csv('./data/data.csv')
        self.data = df.to_dict('records')
        self.__keys = [
            'id',
            'name',
            'status',
            'country',
            'status',
            'reactor_type',
            'reactor_model',
            'construction_start',
            'operational_from',
            'operational_to',
            'capacity',
            'source',
        ]
    
    @property
    def keys(self):
        return self.__keys
    
    @keys.setter
    def keys(self, value):
        return Exception('Cannot modify keys')


    def _init_dict(self, keys:list):
        return dict(zip(keys, [[] for _ in range(len(keys))]))

    def query(self, key:str, value:str)->list[dict]:
        if type(key) == str:
            key = key.lower().replace(" ", "").replace("+", "")
        if type(value) == str:
            value = value.lower().replace(" ", "").replace("+", "")
        
        results = []
        for row in self.data:
            if type(row[key]) == str:
                normalized_key = row[key].lower().replace(" ", "").replace("+", "")
            else:
                normalized_key = row[key]
            if normalized_key == value:
                results.append(row)
                
        return results
    
    def unique(self, key:str)->list:
        if type(key) == str:
            key = key.lower().replace(" ", "").replace("+", "")
        
        results = []
        for row in self.data:
            if row[key] not in results:
                results.append(row[key])
                
        return results
    
    
    def count(self, key:str)->int:
        values = self.unique(key)
        
        result = self._init_dict(values)
        for value in values:
            result[value] = len(self.query(key, value))
            
        return result
            
        
    def group_by(self, key_column:str, columns:list[str])->dict:
        if type(key_column) == str:
            key_column = key_column.lower().replace(" ", "").replace("+", "")
            
        unique_keys = self.unique(key_column)
        
        result = self._init_dict(unique_keys)
        for key in unique_keys:
            for column in columns:
                result[key].append((column, self.count(column)))
            
                
        return result


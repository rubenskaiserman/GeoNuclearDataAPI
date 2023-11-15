import pandas as pd

class Client:
    def __init__(self):
        df = pd.read_csv('./data/data.csv')
        self.data = df.to_dict('records')
        

    def query(self, key:str, value:str)->list[dict]:
        key = key.lower()
        value = value.lower()
        
        results = []
        for row in self.data:
            if row[key].lower() == value:
                results.append(row)
                
        return results
    
    def unique(self, key:str)->list:
        key = key.lower()
        
        results = []
        for row in self.data:
            if row[key] not in results:
                results.append(row[key])
                
        return results
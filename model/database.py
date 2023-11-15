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
    
    
    
if __name__ == '__main__':
    client = Client()
    print(client.data)    
    
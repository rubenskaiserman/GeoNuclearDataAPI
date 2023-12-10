import database
import json
import pandas as pd
import itertools

class Analysis:
    def __init__(self):
        self.db = database.Client()
        
            
    def _query_all(self, key:str, items:list):
        result = []
        for item in items:
            result += self.db.query(key=key, value=item)
        
        return result
    
    
    def _gather_data(self, 
            names:list=[], 
            status:list=[], 
            country:list=[], 
            reactor_type:list=[], 
            reactor_model:list=[],
            capacity:int=0,
        ):
        
        data = dict()
        
        if len(names) > 0:
            data['names'] = self._query_all('name' , names)
            
        if len(status) > 0:
            data['status'] = self._query_all('status' , status)
            
        if len(country) > 0:
            data['country'] = self._query_all('country' , country)
            
        if len(reactor_type) > 0:
            data['reactor_type'] = self._query_all('reactor_type' , reactor_type)
            
        if len(reactor_model) > 0:
            data['reactor_model'] = self._query_all('reactor_model' , reactor_model)
            
        if capacity > 0:
            data['capacity'] = self._query_all('capacity' , capacity)
            
        return data
    
    
    def _intersection(self, data):
        all_ids = []
        for key in data.keys():
            all_ids += [row['id'] for row in data[key]]
            
        unique_ids = set(all_ids)
        
        intersection_ids = []
        for id in unique_ids:
            if all_ids.count(id) == len(data.keys()):
                intersection_ids.append(id)
                
        intersection_data = []
        for id in intersection_ids:
            intersection_data.append(self.db.query('id', id)[0])    
            
        return intersection_data
        
    
    def tables(self, data:dict):
        intersection = []
        
        len_data = len(data.keys())
        for combination_numbers in range(2, len_data+1):
            combinations = itertools.combinations(data.keys(), combination_numbers)
            for combination in combinations:
                intersection.append(self._intersection({key:data[key] for key in combination}))
                
        for table in intersection:
            if len(table) > 0:
                df = pd.DataFrame(table)
                
                print(df)
        
        
            
        
    
    
    # Preciso receber listas de valores para plotar
    def plot(self, 
            names:list=[], 
            status:list=[], 
            country:list=[], 
            reactor_type:list=[], 
            reactor_model:list=[],
            capacity:int=0,
        ):  
        
        data = self._gather_data(
            names=names, 
            status=status, 
            country=country, 
            reactor_type=reactor_type, 
            reactor_model=reactor_model,
            capacity=capacity,
        )    
        
        tables = self.tables(data)
        
        # print(tables)
        
            
            
        # print(json.dumps(self._intersection(data), indent=4))
            

teste = Analysis()

# teste.plot(names=[
#     "Leibstadt",
#     "Columbia (WNP-2)",
#     "Asco-1",
#     "Kola-4",
#     "Paks-2",
#     "LaSalle-2",
#     "Bruce-6",
#     "Cruas-3",
#     "Chinon-B2",
#     "Maanshan-1",
#     "Koeberg-1",
#     "Gundremmingen-B",
#     "Sendai-1",
# ])

teste.plot(
    country=["Pakistan"], 
    status=["Shutdown"], 
    # reactor_type=["PWR"], 
    # reactor_model=["PHWR KWU"], 
)

# names=[
#     "Leibstadt",
#     "Columbia (WNP-2)",
#     "Asco-1",
#     "Kola-4",
#     "Paks-2",
#     "LaSalle-2",
#     "Bruce-6",
#     "Cruas-3",
#     "Chinon-B2",
#     "Maanshan-1",
#     "Koeberg-1",
#     "Gundremmingen-B",
#     "Sendai-1",
# ]

# print(list(itertools.combinations(names, 2)))
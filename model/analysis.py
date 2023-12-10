from model import database
import json
import pandas as pd
import itertools
from matplotlib import pyplot as plt

class Analysis:
    def __init__(self):
        self.db = database.Client()
        
            
    def _query_all(self, key:str, items:list):
        result = []
        for item in items:
            result += self.db.query(key=key, value=item)
        
        return result
    
    
    def _gather_data(self, 
            name:list=[], 
            status:list=[], 
            country:list=[], 
            reactor_type:list=[], 
            reactor_model:list=[],
            capacity:int=0,
        ):
        
        data = dict()
        
        if len(name) > 0:
            data['name'] = self._query_all('name' , name)
            
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


    def _gather_intersection_data(self, data):
        intersection = []
        
        len_data = len(data.keys())
        for combination_numbers in range(1, len_data+1):
            combinations = itertools.combinations(data.keys(), combination_numbers)
            for combination in combinations:
                intersection.append(
                    self._intersection({key:data[key] for key in combination})
                )
        
        return intersection
    
    
    def tables(self, data:dict):
        intersection = self._gather_intersection_data(data)
        
        tables = []        
        
        for table in intersection:
            if len(table) > 0:
                df = pd.DataFrame(table)
                tables.append(df.to_html(
                    classes='my-12 mx-auto w-1/2 text-sm', 
                    border=1, 
                    index=False, 
                    justify='center'
                ))
                
        return tables
  
    def graphs(self, data:dict):
        intersection = self._gather_intersection_data(data)
        

    def analyze(self, 
            name:list=[], 
            status:list=[], 
            country:list=[], 
            reactor_type:list=[], 
            reactor_model:list=[],
            capacity:int=0,
        ):  
        
        data = self._gather_data(
            name=name, 
            status=status, 
            country=country, 
            reactor_type=reactor_type, 
            reactor_model=reactor_model,
            capacity=capacity,
        )    
        
        tables = self.tables(data)
        
        return {
            'tables': tables,
        }
            

if __name__ == '__main__':
    teste = Analysis()

    teste.analyze(
        country=["Pakistan"], 
        status=["Shutdown"], 
        # reactor_type=["PWR"], 
        # reactor_model=["PHWR KWU"], 
    )


import pandas as pd
from abc import ABC, abstractmethod
from model import wikicrawler
import io
import csv

class Database(ABC):
    @abstractmethod
    def query(self, key:str, value:str)->list[dict]:
        pass
    
    @abstractmethod
    def unique(self, key:str)->list:
        pass
    
    @abstractmethod
    def count(self, key:str)->int:
        pass
    
    @abstractmethod
    def group_by(self, key_column:str, columns:list[str])->dict:
        pass

class Client(Database):
    def __init__(self):
        self.wikicrawler = wikicrawler.Webcrawler()
        self.wikicrawler.generate_csv_data()
        csv_data = self.wikicrawler.csv_string
        csv_buffer = io.StringIO(csv_data)
        
        df = pd.read_csv(csv_buffer)
        self.data = df.to_dict('records')
        self.__keys = [
            'id',
            'name',
            'status',
            'country',
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
            if row[key] not in results and str(row[key]) != 'nan':
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

    def query_by_range(self, key:str, min:int, max:int)->list[dict]:
        if type(key) == str:
            key = key.lower().replace(" ", "").replace("+", "")
        
        results = []
        for row in self.data:
            if min <= row[key] <= max:
                results.append(row)
                
        return results

    def update(self):
        self.wikicrawler = wikicrawler.Webcrawler()
        wikicrawler.generate_csv_data()
        csv_data = self.wikicrawler.csv_string
        csv_buffer = io.StringIO(csv_data)
        
        df = pd.read_csv(csv_buffer)
        self.data = df.to_dict('records')
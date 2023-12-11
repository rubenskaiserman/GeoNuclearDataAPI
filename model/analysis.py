from model import database
# import database

import json
import pandas as pd
import itertools
from matplotlib import pyplot as plt
from io import BytesIO
import base64

class Analysis:
    def __init__(self):
        self.db = database.Client()
        
            
    def _query_all(self, key:str, items:list):
        self.db.start()
        if key == 'capacity':
            result = self.db.query_by_range(key=key, min=items - 1000, max=items + 1000)
                
            return result
        
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
        self.db.start()
        data = {'parameters': dict()}
        
        if len(name) > 0:
            data['name'] = self._query_all('name' , name)
            data['parameters']['name'] = name
            
        if len(status) > 0:
            data['status'] = self._query_all('status' , status)
            data['parameters']['status'] = status
            
        if len(country) > 0:
            data['country'] = self._query_all('country' , country)
            data['parameters']['country'] = country
            
        if len(reactor_type) > 0:
            data['reactor_type'] = self._query_all('reactor_type' , reactor_type)
            data['parameters']['reactor_type'] = reactor_type
            
        if len(reactor_model) > 0:
            data['reactor_model'] = self._query_all('reactor_model' , reactor_model)
            data['parameters']['reactor_model'] = reactor_model
            
        if capacity > 0:
            data['capacity'] = self._query_all('capacity' , capacity)
            data['parameters']['capacity'] = capacity
            
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
        self.db.start()
        for id in intersection_ids:
            intersection_data.append(self.db.query('id', id)[0])    
            
        return intersection_data


    def _gather_intersection_data(self, data):
        intersection = []
        
        len_data = len(data.keys())
        for combination_numbers in range(1, len_data+1):
            keys = list(data.keys())
            keys.remove('parameters')
            combinations = itertools.combinations(keys, combination_numbers)
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
                df.drop(columns=['source', 'iaeaid', 'last_updated'], inplace=True)
                
                tables.append(df.to_html(
                    classes='my-12 mx-auto w-1/2 text-sm',
                    col_space=100,
                    border=1, 
                    index=False, 
                    justify='center'
                ))
                
        print(len(tables))
        
        return tables

    def _save_graph(self, graph:plt)->base64:
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)     
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        
        return image_base64

    # Multiplos nomes => Quais foram os tipos de reatores selecionadas
    def graphs(self, by:str, data:dict):
        images = []
        
        if by == 'name':
            results = data['name']
            df = pd.DataFrame(results)
            df = df.sort_values(by=['capacity'], ascending=False)
            x = df['name'].tolist()
            y = df['capacity'].tolist()
            
            if len(x) < 10:
                plt.bar(x, y)
                plt.xticks(rotation=-25, ha='left', fontsize=8)
                plt.xlabel('Reactor Name', labelpad=10, fontsize=12)
            else:
                plt.bar([_ for _ in range(len(x))], y, linewidth=2, fill=True)
                plt.xticks(fontsize=0)
                plt.xlabel('Reactor Space', labelpad=10, fontsize=12)
                
            plt.ylabel('Capacity (MW)')   
            plt.title('Reactor Capacity') 
            graph = self._save_graph(plt)
            plt.close()
            
            images.append(graph) 
            
            # 100% Gambiarra. Tenho sono e não quero pensar em como fazer isso de forma correta.
            countries = df['country'].unique()
            y = [df['country'].tolist().count(country) for country in countries]
            countries_and_y = list(zip(countries, y))
            df = pd.DataFrame(countries_and_y, columns=['country', 'count'])
            df = df.sort_values(by=['count'], ascending=False)
            countries = df['country'].tolist()
            y = df['count'].tolist()
            
            if len(countries) < 6:
                plt.pie(
                    y, 
                    labels=[country for country in countries], 
                    autopct='%1.1f%%', 
                    shadow=False, 
                    startangle=90,
                )
            else: 
                plt.bar(countries, y)
                plt.xticks(rotation=-25, ha='left', fontsize=8)
                plt.xlabel('Country', labelpad=10, fontsize=12)
                plt.ylabel('Number of Reactors')
            
            plt.title('Countries Selected')
            graph = self._save_graph(plt)
            plt.close()
            
            images.append(graph)
            
            return images
        
        
        
        
        
        
        if by == 'status':
            pass
        if by == 'country':
            pass
        if by == 'reactor_type':
            pass
        if by == 'reactor_model':
            pass
        if by == 'capacity':
            pass
    
    # Multiplos status => Quantidade de reatores por status
    # Multiplos status => Status Por país
    # Multiplos status => Status por tipo de reator
    # Multiplos status => Status por modelo de reator
    # Multiplos status => Status por capacidade de reator
    
    # Multiplos países => Quantidade de reatores por país
    # Multiplos países => Países por status
    # Multiplos países => Países por tipo de reator
    # Multiplos países => Países por modelo de reator
    # Multiplos países => Países por capacidade de reator
    # Multiplos países => Soma da energia por país
    # Multiplos países => Soma da energia por tipo de reator
    # Multiplos países => Soma da energia por modelo de reator
    
    # Multiplos tipos de reator => Quantidade de reatores por tipo de reator
    # Multiplos tipos de reator => Tipos de reator por status
    # Multiplos tipos de reator => Tipos de reator por país
    # Multiplos tipos de reator => Tipos de reator por modelo de reator
    # Multiplos tipos de reator => Tipos de reator por capacidade de reator
    # Multiplos tipos de reator => Soma da energia por tipo de reator
    
    # Multiplos modelos de reator => Quantidade de reatores por modelo de reator
    # Multiplos modelos de reator => Modelos de reator por status
    # Multiplos modelos de reator => Modelos de reator por país
    # Multiplos modelos de reator => Modelos de reator por tipo de reator
    # Multiplos modelos de reator => Modelos de reator por capacidade de reator
    # Multiplos modelos de reator => Soma da energia por modelo de reator
    
    # Capacidade de reator => Quantidade de reatores por capacidade de reator
    # Capacidade de reator => Capacidade de reator por status
    # Capacidade de reator => Capacidade de reator por país
    # Capacidade de reator => Capacidade de reator por tipo de reator
    # Capacidade de reator => Capacidade de reator por modelo de reator
    
    # Multiplos de alguma coluna com unidade de outra coluna segue os critérios da coluna que contém multiplos, mas limitada pela coluna com unidade.
    
    # Valor Ùnico de multiplas colunas => Mostrar todos os comparativos possíveis dentro da interseção dos valores
    
    # Multiplos de Multiplas Colunas => Mostrar todos os comparativos possíveis dentro da interseção dos valores
        
        

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
        
        graphs = []
        if len(name) > 1 and capacity == 0:
            graphs = self.graphs(by='name', data=data)
            return {
                'tables': tables,
                'graphs': graphs,
            }
        
        
        
        return {
            'tables': tables,
        }
            

if __name__ == '__main__':
    teste = Analysis()

    teste.analyze(
        name=['Fangchenggang-3', 'Hongyanhe-5'],
        country=["Pakistan"], 
        # status=["Shutdown"], 
        # reactor_type=["PWR"], 
        # reactor_model=["PHWR KWU"], 
    )


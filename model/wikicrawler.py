from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
import csv

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

# browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

import time


# Classe que atualiza o arquivo data.csv quando instanciada.
class Webcrawler:
    def __init__(self):
        steps = 1
        
        # XPath modular que define cada tabela da página
        self.__default_xpath = "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/table[%%]"

        # Instanciação do objeto Webdriver que coleta os dados
        options = ChromeOptions()
        options.headless = True
        print(chromedriver_binary.chromedriver_filename)
        self.webdriver = Chrome(executable_path=chromedriver_binary.chromedriver_filename, options=chrome_options)

        self.tables = list()
        try:
            # Método que acessa a página da Wikipedia
            self.webdriver.get("https://en.wikipedia.org/wiki/List_of_commercial_nuclear_reactors")

            # Coleta dos países presentes na página
            self.countries = [item.text for item in self.webdriver.find_elements(By.CLASS_NAME, "mw-headline")[:-4]]

            # Acesso e coleta dos dados de cada tabela
            for index in range(1, len(self.countries) + 1):
                print(f"Step: {steps}")
                steps +=1
                
                table = self.webdriver.find_element(By.XPATH, self.__default_xpath.replace("%%", str(index)))
                rows = table.find_elements(By.XPATH, "./tbody/tr")
                tlist = self.format_table_list(rows)
                self.tables.append(tlist)

            # Montagem de uma lista com os dados completos de cada reator
            self.full_data = self.assemble_full_data()

            # Montagem do arquivo data.csv
            self.assemble_csv_file("./data/data1")
        finally:

            # Fechamento do navegador
            self.webdriver.close()

    @property
    def default_xpath(self):
        return self.__default_xpath

    @default_xpath.setter
    def default_xpath(self, value):
        raise Exception("Default XPath can't be altered.")

    # Método que realiza a refatoração das unidades de cada usina que não têm os dados completos.
    @staticmethod
    def include_plant_name(tlist: list[list]) -> list:
        if length := len(tlist[0]) > 9:
            tlist = [item[:9-length] for item in tlist]
        new_list = list()
        for index, element in enumerate(tlist):
            if len(element) == 9:
                new_list.append(element)
            else:
                if element[1] == '1':
                    element.append('')
                else:
                    element.insert(0, tlist[index-1][0])
                    new_list.append(element)
        return new_list

    # Método que transforma cada tabela em uma lista de todos os reatores.
    def format_table_list(self, rows) -> list:
        start = time.time() 
        
        tlist = list()
        for row in rows:
            data = list()
            for item in row.find_elements(By.XPATH, './td'):
                item = item.text
                if '[' in item:
                    index = item.index('[')
                    item = item[:index]
                data.append(item)
            tlist.append(data)
        tlist = self.include_plant_name(tlist)
        for unit in tlist:
            capacity = unit[5]
            if '\n' in capacity:
                parsed = capacity.split('\n')
                parsed = [float(value) for value in parsed]
                average_capacity = sum(parsed)/len(parsed)
                unit[5] = average_capacity
            if capacity == '':
                unit[5] = 0
            else:
                unit[5] = float(unit[5])
                
            end = time.time()
            print(f"Time: {end-start}")    
            
        return tlist

    # Método que constroi a lista com todos os reatores separados
    def assemble_full_data(self):
        full_data_list = list()
        if len(self.countries) != len(self.tables):
            raise Exception("Mismatch between number of countries and tables.")
        for index, country in enumerate(self.tables):
            for plant in country:
                plant.insert(0, self.countries[index])
                full_data_list.append(plant)
        return full_data_list

    # Método que escreve o arquivo data.csv
    def assemble_csv_file(self, fpath: str):
        with open(f'{fpath}.csv', 'w+', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            fields = ['id', 'name', 'country', 'status', 'reactor_type', 'reactor_model', 'construction_start',
                      'operational_from', 'operational_to', 'capacity', 'last_updated', 'source', 'iaeaid']
            writer.writerow(fields)
            for index in range(len(self.full_data)):
                row = self.make_csv_row(self.full_data[index], index)
                writer.writerow(row)
            csvfile.close()

    # Método que reordena e adiciona os valores para o registro do arquivo data.csv
    @staticmethod
    def make_csv_row(rdata: list, idd: int) -> list:
        newlist = [idd, rdata[1]+'-'+rdata[2], rdata[0], rdata[5], rdata[3], rdata[4], rdata[7], rdata[8], rdata[9],
                   rdata[6], '', '', '']
        return newlist


if __name__ == "__main__":
    obj = Webcrawler()
import requests
from bs4 import BeautifulSoup
import csv
import time
import csv
import io


# Classe que atualiza o arquivo data.csv quando instanciada.
class Webcrawler:
    def generate_csv_data(self):
        steps = 1

        self.__default_xpath = "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/table[%%]"

        try:
            # Realiza a request e obtém o conteúdo HTML
            response = requests.get('https://en.wikipedia.org/wiki/List_of_commercial_nuclear_reactors')
            
            soup = BeautifulSoup(response.text, 'html.parser')

            # print(soup)
            # Coleta dos países presentes na página
            self.countries = [item.text for item in soup.find_all('span', {'class': 'mw-headline'})[:-4]]
            

            # Acesso e coleta dos dados de cada tabela
            self.tables = []
            for index in range(1, len(self.countries) + 1):
                table = soup.find_all('table', {'class': 'wikitable'})
                rows = table[index - 1].find_all('tr')
                print("Rows separated")
                tlist = self.format_table_list(rows)
                print("Tlist separated")
                self.tables.append(tlist)

                print(f"Step: {steps}")
                steps += 1

            # Montagem de uma lista com os dados completos de cada reator
            self.full_data = self.assemble_full_data()

            # Montagem do arquivo data.csv
            temp_csv_string = self.assemble_csv_string()
            self.__csv_string = temp_csv_string
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("Execution complete.")

    @property
    def csv_string(self):
        return self.__csv_string

    @property
    def default_xpath(self):
        return self.__default_xpath

    @default_xpath.setter
    def default_xpath(self, value):
        raise Exception("Default XPath can't be altered.")

    @staticmethod
    def include_plant_name(tlist: list[list]) -> list:
        tlist.pop(0)
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

    def format_table_list(self, rows) -> list:
        start = time.time()

        tlist = list()
        for row in rows:
            data = [item.get_text(strip=True) for item in row.find_all(['td', 'th'])]
            tlist.append(data)

        tlist = self.include_plant_name(tlist)
        for unit in tlist:
            capacity = unit[5]
            if '\n' in capacity:
                parsed = capacity.split('\n')
                new_parsed = []
                print(parsed)
                for value in parsed:
                    if '[' in value:
                        value = value[:value.index('[')]
                    new_parsed.append(float(value))
                parsed = new_parsed
                average_capacity = sum(parsed)/len(parsed)
                unit[5] = average_capacity
            if capacity == '':
                unit[5] = 0
            else:
                if '[' in unit[5]:
                    unit[5] = unit[5][:unit[5].index('[')]
                unit[5] = float(unit[5])
                
            end = time.time()
            print(f"Time: {end-start}")

        return tlist

    def assemble_full_data(self):
        full_data_list = list()
        if len(self.countries) != len(self.tables):
            raise Exception("Mismatch between number of countries and tables.")
        for index, country in enumerate(self.tables):
            for plant in country:
                plant.insert(0, self.countries[index])
                full_data_list.append(plant)
        return full_data_list

    def assemble_csv_string(self):
        csv_string_io = io.StringIO()
        writer = csv.writer(csv_string_io)
        
        fields = ['id', 'name', 'country', 'status', 'reactor_type', 'reactor_model', 'construction_start',
                'operational_from', 'operational_to', 'capacity', 'last_updated', 'source', 'iaeaid']
        writer.writerow(fields)

        for index in range(len(self.full_data)):
            row = self.make_csv_row(self.full_data[index], index)
            writer.writerow(row)

        csv_content = csv_string_io.getvalue()
        csv_string_io.close()

        return csv_content


    @staticmethod
    def make_csv_row(rdata: list, idd: int) -> list:
        newlist = [idd, rdata[1]+'-'+rdata[2], rdata[0], rdata[5], rdata[3], rdata[4], rdata[7], rdata[8], rdata[9],
                   rdata[6], '', '', '']
        return newlist


if __name__ == "__main__":
    obj = Webcrawler()

# GeoNuclearDataAPI

### Criação de Virtual Environment para instalação de dependências do projeto
```
    python3 -m venv venv
```
OBS: Geralmente no windows o comando é python ao invés de python3

### Seleção de ambiente virtual como executor do código python
```
    source <diretório do projeto>/venv/bin/activate
``` 
Source pode não ser o comando do windows.
Se preferir por apertar ctrl + shift + p e buscar por Python: Select Interpreter
Daí selecione o venv

### Instalando as dependências no ambiente virtual
```
    pip install -r requirements.txt
```
Lembrando que isso deve ser executado em um terminal e você deve estar dentro da pasta do projeto
com o interpretador do ambiente virtual selecionado. Do contrário as dependencias serão instaladas 
na sua máquina local.

### Executando o projeto
```
    python3 <diretório do projeto>/index.py
```
Ou pode clicar pra executar o arquivo main no vscode

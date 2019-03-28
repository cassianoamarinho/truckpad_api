# truckpad_api
  Teste Tecnico para vaga de backend
 
### Requisitos
  * Python 3.6
  * pipenv
  
### Configuração
  * Na pasta raiz do projeto executar o comando 'pipenv install'
  * Na pasta raiz do projeto executar o comando 'pipenv run python start.py db init'
  * Na pasta raiz do projeto executar o comando 'pipenv run python start.py db migrate'
  * Na pasta raiz do projeto executar o comando 'pipenv run python start.py db upgrade'
  
### Rodar o projeto
  * Para rodar os testes execute o comando 'TRUCKPAD_ENV=test pipenv run pytest --junitxml results.xml'
  * Para subir o servidor execute o comando 'pipenv run python start.py runserver'
  
### Endpoints
* JSON de exemplo:
      ``` 
           { 
            "id": "ad2a14a2-3be5-425b-a4aa-6f399444a2c7",
            "name": "Motorista",
            "born_date": "1992-06-29",
            "gender": 2,
            "has_truck": False,
            "is_loaded": True,
            "cnh_type": "D",
            "truck_type": 4,
            "origin_city": "São Paulo",
            "origin_state": "SP",
            "destination_city": "Rio de Janeiro",
            "destination_state": "RJ"
           } ```

  * ```POST /drivers```
  * ```PUT /drivers/<driver_id>```
  * ```DELETE /drivers/<driver_id>```
  * ```GET /drivers/<driver_id>```
  * ```GET /drivers/has_truck/count```
  * ```GET /drivers/is_loaded/false```
  * ```GET /drivers/truck_types/list```
  * ```GET /drivers/period```
  
  
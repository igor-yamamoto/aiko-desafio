# Desafio Back-end - Estágio Aiko 2020

Este repositório contém a minha solução para o teste de Back-end development referente ao processo seletivo de estágio 2020 da Aiko.

O desafio consiste no desenvolvimento de uma API com a implementação de operações CRUD sobre tabelas que monitoram e descrevem um sistema de transporte, similar ao [API Olho Vivo](https://github.com/aikodigital/programa-estagio/blob/master/api.md). Maiores detalhes sobre o desafio podem ser encontrados [no repositório](https://github.com/aikodigital/programa-estagio/blob/master/back-end.md).

## Configuração
Este projeto foi desenvolvido utilizando as ferramentas do pacote Django e Django REST Framework. A RDBMS utilizada foi PostgreSQL, mas os mesmos resultados podem ser obtidos através do uso de qualquer banco de dados relacional.

Para fazer uso da API:
* Clone este repositório à sua máquina
* Acesse o diretório através do comando `cd teste/back-end/igor`
* Instale as dependências com `pip3 install -r requirements.txt`
* Acesse o diretório da aplicação por meio do comando `cd aiko`
* No arquivo `aiko/settings.py`, configure as informações de usuários PostgreSQL. Nele, devem ser substituidos os campos `'USER'` e `'PASSWORD''` pelo usuário e senha, respectivamente 
	* O banco de dados configurado por padrão tem o nome `aikodb`. Portanto, acesse o seu terminal PostgreSQL (com o mesmo usuário especificado em `'USER'`) e entre o comando `CREATE DATABASE aikodb;`
* Migre os modelos usando o comando `python3 manage.py makemigrations` e então `python3 manage.py migrate`
* O servidor pode ser inicializado através do comando `python3 manage.py runserver`. O acesso pode ser feito pelo endereço [localhost:8000/](http://localhost:8000/)

### Acesso por meio do Docker
Este projeto também foi containerizado. Para fazer uso da API por meio do Docker:
* Acesse o arquivo `docker-compose.yml` e configure os campos `POSTGRES_USER` e `POSTGRES_PASSWORD` com o seu usuário e senha PostgreSQL, respectivamente
* O host configurado no arquivo do docker compose leva o nome `db`. Assim, este nome precisa também ser passado ao arquivo `aiko/aiko/settings.py`. Para não perder informações da configuração local, a lista `DBS` contém duas configurações do banco de dados, uma para uso através do Docker (índice `0`) e outra para uso através de configurações locais (índice `1`). Por padrão, este projeto está configurado para uso das configurações locais, e portanto, caso seja utilizado com o Docker, mude a linha `DATABASES = DBS[1]` para `DATABASES = DBS[0]`
	* Configure o nome do usuário e a senha PostgreSQL nos campos `'USER'` e `'PASSWORD'` pelos mesmos configurados no arquivo `docker-compose.yml`
* Migre os modelos com o comando `sudo docker-compose run api python3 aiko/manage.py migrate`. Aqui, ao Docker já será feito um build
* O servidor pode ser inicializado através do comando `sudo docker-compose up`. O acesso pode ser feito pelo endereço [localhost:8000/](http://localhost:8000/)

## Uso da API



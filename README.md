# Desafio Back-end - Estágio Aiko 2020

Este repositório contém a minha solução para o teste de Back-end development referente ao processo seletivo de estágio 2020 da Aiko.

O desafio consiste no desenvolvimento de uma API com a implementação de operações CRUD sobre tabelas que monitoram e descrevem um sistema de transporte, similar ao [API Olho Vivo](https://github.com/aikodigital/programa-estagio/blob/master/api.md). Maiores detalhes sobre o desafio podem ser encontrados [no repositório](https://github.com/aikodigital/programa-estagio/blob/master/back-end.md).

## Configuração
Este projeto foi desenvolvido utilizando as ferramentas do pacote Django e Django REST Framework. A RDBMS utilizada foi PostgreSQL, mas os mesmos resultados podem ser obtidos através do uso de qualquer banco de dados relacional.

Para fazer uso da API:
* Clone este repositório à sua máquina
* Acesse o diretório através do comando `cd teste/back-end/igor`
* Inicie um ambiente virtual e instale as dependências com o comando `pip3 install -r requirements.txt`
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
A API consiste de quatro tabelas. São elas:
* **Paradas**: Relação de todas as paradas registradas no sistema. Consiste de um id (`id`: `primary key - long`), nome (`name_parada`: `char(50)`), latitude (`lat_parada`: `bigint`) e longitude (`long_parada`: `bigint`)
* **Linhas**: Relação de todas as linhas registradas no sistema. Consiste de um id (`id`: `primary key - long`), nome (`name_linha`: `char(50)`) e uma chave externa das paradas registradas (`foreign key - many to many`).
* **Veiculos**: Relação de todas os veiculos registrados no sistema. Consiste de um id (`id`: `primary key - long`), nome (`name_veiculo`: `char(30)`), modelo (`model_veiculo`: `char(30)`) e uma chave externa das linhas registradas (`foreign key - many to one`).
* **Posição dos veiculos**: Relação da posição de todos os veiculos registrados no sistema. Consiste de latitude (`lat_veiculo`: `bigint`), longitude (`long_veiculo`: `bigint`) e uma chave externa dos veiculos registrados, que também serve de chave primária (`foreign key - one to one`).

Ao rodar o servidor e acessar o endereço [localhost:8000/](http://localhost:8000/), o usuário é apresentado ao template de inicialização do Swagger. Nesta página, é possível realizar diversas operações, como `GET`, `POST`, `PUT` e `DELETE`. Também, é possível realizar a operação de `PATCH` em algumas tabelas.

Os métodos principais são `/api/{modelo}` e `/api/{modelo}/id:{primary_key}/`. Nos campos entre chaves (`{ }`) devem ser substituidos strings que conferem o acesso a cada uma das tabelas apresentadas acima. A relação completa de url's é:
* [/api/veiculos/](http://localhost:8000/api/veiculos/): url associada à tabela de veiculos. 
* [/api/linhas/](http://localhost:8000/api/linhas/): url associada à tabela de linhas. 
* [/api/paradas/](http://localhost:8000/api/paradas/): url associada à tabela de paradas. 
* [/api/posicaoveiculos/](http://localhost:8000/api/posicaoveiculos/): url associada à tabela de posição dos veiculos. 
	* Todas as url's acima suportam as operações de `GET` (lista todas as insâncias da tabela), `POST` (insere novas instâncias na base de dados), `DELETE` (deleta todas as instancias da tabela)

Se qualquer uma das url's descritas acima forem acompanhadas de um `id`, é possível fazer uma das operações dentre `GET`, `PUT`, `PATCH` e `DELETE`. Por exemplo, a operação de `GET` sobre `/api/veiculos/id:1/` retorna a instância contida na tabela `api_veiculo` descrita pelo `id` igual a 1.

A API também conta com três outros métodos além dos que já foram descritos. Estes são:
* [/api/paradaslinhas/](http://localhost:8000/api/paradaslinhas/): url que provê acesso às paradas, acompanhadas de todas as linhas associadas.
* [/api/linhasveiculos/](http://localhost:8000/api/linhasveiculos/): url que provê acesso às linhas, acompanhadas de todas os veiculos associados.
	* As duas url's acima suportam a operação 'GET' (listagem de todas as instnâcias)
	* O acesso à instâncias específicas pode ser feito pelas urls `/api/paradaslinhas/id:{parada_id}/` ou `/api/linhasveiculos/id:{linha_id}`. Estes métodos suportam as operações `GET` (acesso à isntância), `PUT` (atualização de toda a instância) e `PATCH` (atualização apenas de campos específicos)
* `/api/paradasposicao/{lat}:{lon}/`: url que retorna as três paradas mais próximas às coordenadas passadas
	* Caso deseje-se acessar as `N` paradas mais próximas às coordenadas, utiliza-se a url `/api/paradasposicao/{lat}:{lon}/n:{n_paradas}`




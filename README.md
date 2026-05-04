# ⚡Curso FastAPI 
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
> Este repositório contém o código desenvolvido durante o curso

Curso ministrado por [@dunossauro](https://github.com/dunossauro), que teve como objetivo desenvolver na prática APIs modernas utilizando o **FastAPI**.

## Tópicos abordados no curso
 - Configurar e gerenciamento ambiente do projeto;
 - Conceitos do desenvolvimento web com FastAPI;
 - Modelagem de dados;
 - Migrações;
 - Autenticação e Autorização com JWT;
 - Testes unitários;
 - Programação Assíncrona;
 - Conteinerização; e
 - Deploy da Aplicação FastAPI.
   
## Sobre o framework
Resumidamente o FastAPI é framework moderno, rápido e eficiente para desenvolvimento backend em Python.
Sua principal característica é a geração automática de documentação (OpenAPI) e possui tipagem estática. 
Principais aplicabilidade é em APIs REST, WebSockets e Arquiteturas orientadas a eventos.

## Configuração e gerenciamento de ambiente
Para curso foi utilizado o ![Poetry](https://img.shields.io/badge/dependencies-Poetry-60A5FA?logo=poetry) para gerenciar o ambiente virtaul de desenvolvimento, controlar as versões de dependências.
Cabe destacar que, o poetry é mais completo em comparação com o ambiente virtual natio do python, o venv.

## Visão geral do curso
Durante o curso foi apresentado os métodos HTTP como o `GET` que solicita um dado já existente; o `PUT` que atualiza um recurso existente; o `POST` que	cria um novo recurso e o `DELETE` que exclui um recurso, esses métodos são essenciais para comunicação cliente-servidor.

Em seguida foram abordados os "status code" que são respostas (responses) que o servidor pode retornar, como por exemplo o erro `500` que significa erro interno do servidor.

Na aula de modelagem de dados, adquiri conceitos valiosos e tive o primeiro contato com ORM SQLAlchemy. Esse ORM faz o mapeamento objeto-relacional, abstrai de queries SQL e manipula entidades como objetos Python. Ainda, na mesma aula foram abordadas as migrações que versiona o banco de dados, controla a evolução do schema e também pode reverter operações.

Em seguida, implementamos a autenticação de usuários com Json Web Token (JWT), bem como a proteção dos endpoints com o OAuth2Password.

🚧 Continua...

## Tecnologias

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red)
![Pydantic](https://img.shields.io/badge/Data%20Validation-Pydantic-blueviolet)
![Tests](https://img.shields.io/badge/tests-pytest-green)
![SQLite](https://img.shields.io/badge/database-SQLite-07405E)

---

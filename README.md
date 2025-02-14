# API de Gerenciamento de Empresas e Obrigações Acessórias

Este projeto é uma API desenvolvida com FastAPI, SQLAlchemy e Pydantic para gerenciar empresas e suas obrigações acessórias.

## Tecnologias Utilizadas

- **Python 3.11**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **PostgreSQL**
- **Uvicorn**

## Instalação e Configuração

### 1. Clonar o Repositório

```sh
git clone https://github.com/HenriSousa/desafio-api.git
cd desafio-api
```

### 2. Criar e Ativar um Ambiente Virtual

```sh
python -m venv venv
# No Windows
venv\Scripts\activate
# No Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependências

```sh
pip install -r requirements.txt
```

### 4. Configurar o Banco de Dados

Crie um arquivo `.env` na raiz do projeto com as credenciais do PostgreSQL:

```
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
```

### 5. Criar as Tabelas

Execute o seguinte comando para criar as tabelas no banco de dados:

```sh
python -c "from main import Base, engine; Base.metadata.create_all(bind=engine)"
```

## Diagrama de Classes

``` mermaid

classDiagram
    class Empresa {
        +int id
        +string nome
        +string cnpj
        +string endereco
        +string email
        +string telefone
    }
    
    class ObrigacaoAcessoria {
        +int id
        +string nome
        +string periodicidade
        +int empresa_id
    }
    
    Empresa "1" -- "*" ObrigacaoAcessoria : possui
   
```

## Executando a API

Para iniciar a API, execute:

```sh
uvicorn main:app --host 127.0.0.1 --port 8080 --reload
```

A API estará disponível em:

- **Swagger UI**: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
- **Redoc**: [http://127.0.0.1:8080/redoc](http://127.0.0.1:8080/redoc)

## Endpoints

### Empresas

- **Criar Empresa:** `POST /empresas/`
- **Listar Empresas:** `GET /empresas/`
- **Buscar Empresa por ID:** `GET /empresas/{empresa_id}`
- **Atualizar Empresa:** `PUT /empresas/{empresa_id}`
- **Deletar Empresa:** `DELETE /empresas/{empresa_id}`
- **Listar Empresas com Obrigações:** `GET /empresas_com_obrigacoes/`

### Obrigações Acessórias

- **Criar Obrigação:** `POST /obrigacoes/`
- **Buscar Obrigação por ID:** `GET /obrigacoes/{obrigacao_id}`
- **Atualizar Obrigação:** `PUT /obrigacoes/{obrigacao_id}`
- **Deletar Obrigação:** `DELETE /obrigacoes/{obrigacao_id}`

## Testes

Para rodar os testes, utilize:

```sh
pytest test_main.py
```

## Contato

**Desenvolvedor:** Henrique\
**E-mail:** [henrisousa7@hotmail.com](mailto\:henrisousa7@hotmail.com)


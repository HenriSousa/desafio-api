from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from database import Base, engine
from main import app, get_db

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criando um banco de testes antes de rodar os testes
Base.metadata.create_all(bind=engine)

# Função para substituir a injeção de dependência do banco nos testes
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_empresa():
    response = client.post("/empresas/", json={
        "nome": "Empresa Teste",
        "cnpj": "12345678000195",
        "endereco": "Rua Teste, 123",
        "email": "empresa@teste.com",
        "telefone": "11999999999"
    })
    assert response.status_code == 200  # ou 201 dependendo da implementação
    assert response.json()["nome"] == "Empresa Teste"

def test_get_empresa():
    response = client.get("/empresas/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["nome"] == "Empresa Teste"

def test_get_all_empresas():
    response = client.get("/empresas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Deve retornar uma lista

def test_update_empresa():
    response = client.put("/empresas/1", json={
        "nome": "Empresa Atualizada",
        "cnpj": "12345678000195",
        "endereco": "Rua Nova, 456",
        "email": "empresa@atualizada.com",
        "telefone": "11999999998"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Empresa Atualizada"

def test_delete_empresa():
    response = client.delete("/empresas/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Empresa deletada com sucesso"}

def test_create_obrigacao():
    response = client.post("/obrigacoes/", json={
        "nome": "DCTF",
        "periodicidade": "Mensal",
        "empresa_id": 1
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "DCTF"

def test_get_obrigacao():
    response = client.get("/obrigacoes/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_all_obrigacoes():
    response = client.get("/obrigacoes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_obrigacao():
    response = client.delete("/obrigacoes/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Obrigação deletada com sucesso"}


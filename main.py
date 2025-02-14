from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from empresaModel import Empresa as EmpresaModel
from obrigacaoAcessoriaModel import ObrigacaoAcessoria as ObrigacaoAcessoriaModel
from pydanticModel import EmpresaCreate, Empresa as EmpresaPydantic, ObrigacaoAcessoriaCreate, \
    ObrigacaoAcessoria as ObrigacaoAcessoriaPydantic, EmpresaComObrigacoes

# Criação das tabelas
from empresaModel import Base
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Prova de Seleção de Estágio",
    description="Criar uma API simples utilizando FastAPI, "
                "Pydantic, SQLAlchemy para cadastrar empresas "
                "e gerenciar obrigações acessórias que a empresa "
                "precisa declarar para o governo.",
    version="1.0.0",
    contact={
        "name": "Henrique",
        "email": "henrisousa7@hotmail.com",
    }
    )

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD de Empresa

# Cadastro da empresa http://127.0.0.1:8080/empresas/
@app.post("/empresas/", response_model=EmpresaPydantic, summary="Criar uma empresa", description="Cadastra uma nova empresa na base de dados.")
def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    # Verifica se o CNPJ já existe
    """Registra uma nova empresa, garantindo que o CNPJ não seja duplicado."""
    db_empresa = db.query(EmpresaModel).filter(EmpresaModel.cnpj == empresa.cnpj).first()
    if db_empresa:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado")

    try:
        db_empresa = EmpresaModel(
            nome=empresa.nome,
            cnpj=empresa.cnpj,
            endereco=empresa.endereco,
            email=empresa.email,
            telefone=empresa.telefone
        )
        db.add(db_empresa)
        db.commit()
        db.refresh(db_empresa)
        return db_empresa
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro ao cadastrar empresa. Verifique os dados e tente novamente.")

# Retorna todas as empresas http://127.0.0.1:8080/empresas/
@app.get("/empresas/", response_model=list[EmpresaPydantic], summary="Listar empresas", description="Retorna todas as empresas cadastradas.")
def get_empresas(db: Session = Depends(get_db)):
    """Busca todas as empresas registradas no sistema."""
    empresas = db.query(EmpresaModel).all()
    return empresas

# Retorna todas as empresas junto com suas obrigações http://127.0.0.1:8080/empresas_com_obrigacoes/
@app.get("/empresas_com_obrigacoes/", response_model=list[EmpresaComObrigacoes], summary="Listar empresas com Obrigações", description="Retorna todas as empresas cadastradas com obrigações.")
def get_empresas_com_obrigacoes(db: Session = Depends(get_db)):
    """Busca todas as empresas registradas no sistema com Obrigações."""
    empresas = db.query(EmpresaModel).all()
    return empresas

# Buscar empresa com ID http://127.0.0.1:8080/empresas/{ID}
@app.get("/empresas/{empresa_id}", response_model=EmpresaPydantic, summary="Obter empresa por ID", description="Busca uma empresa pelo seu identificador único.")
def get_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """Retorna os detalhes de uma empresa específica."""
    db_empresa = db.query(EmpresaModel).filter(EmpresaModel.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return db_empresa

# Atualizar dados da empresa http://127.0.0.1:8080/empresas/{ID}
@app.put("/empresas/{empresa_id}", response_model=EmpresaPydantic, summary="Atualizar empresa", description="Atualiza os dados de uma empresa existente.")
def update_empresa(empresa_id: int, empresa: EmpresaCreate, db: Session = Depends(get_db)):
    """Modifica os dados de uma empresa específica."""
    db_empresa = db.query(EmpresaModel).filter(EmpresaModel.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    # Atualiza os campos
    db_empresa.nome = empresa.nome
    db_empresa.cnpj = empresa.cnpj
    db_empresa.endereco = empresa.endereco
    db_empresa.email = empresa.email
    db_empresa.telefone = empresa.telefone

    db.commit()
    db.refresh(db_empresa)
    return db_empresa


# Deletar uma empresa

# Excluir empresa http://127.0.0.1:8080/empresas/{ID}
@app.delete("/empresas/{empresa_id}", response_model=dict, summary="Excluir empresa", description="Remove uma empresa do banco de dados.")
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """Apaga uma empresa da base de dados pelo ID."""
    db_empresa = db.query(EmpresaModel).filter(EmpresaModel.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    db.delete(db_empresa)
    db.commit()
    return {"message": "Empresa deletada com sucesso"}

# CRUD de ObrigacaoAssessoria

# Cadastro de Obrigacao http://127.0.0.1:8080/obrigacoes/
@app.post("/obrigacoes/", response_model=ObrigacaoAcessoriaPydantic, summary="Criar obrigação acessória", description="Cadastra uma nova obrigação acessória vinculada a uma empresa.")
def create_obrigacao(obrigacao: ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    """Registra uma nova obrigação acessória."""
    db_empresa = db.query(EmpresaModel).filter(EmpresaModel.id == obrigacao.empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    db_obrigacao = ObrigacaoAcessoriaModel(
        nome=obrigacao.nome,
        periodicidade=obrigacao.periodicidade,
        empresa_id=obrigacao.empresa_id
    )
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

# Buscar Obrigacao por ID http://127.0.0.1:8080/obrigacoes/{ID}
@app.get("/obrigacoes/{obrigacao_id}", response_model=ObrigacaoAcessoriaPydantic, summary="Obter obrigação por ID", description="Busca uma obrigação acessória pelo seu identificador único.")
def get_obrigacao(obrigacao_id: int, db: Session = Depends(get_db)):
    """Retorna os detalhes de uma obrigação específica."""
    db_obrigacao = db.query(ObrigacaoAcessoriaModel).filter(ObrigacaoAcessoriaModel.id == obrigacao_id).first()
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação Assessória não encontrada")
    return db_obrigacao

# Atualizar obrigacao por ID http://127.0.0.1:8080/obrigacoes/{ID}
@app.put("/obrigacoes/{obrigacao_id}", response_model=ObrigacaoAcessoriaPydantic, summary="Atualizar obrigação", description="Atualiza os dados de uma obrigação acessória existente.")
def update_obrigacao(obrigacao_id: int, obrigacao: ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    """Modifica os dados de uma obrigação acessória específica."""
    db_obrigacao = db.query(ObrigacaoAcessoriaModel).filter(ObrigacaoAcessoriaModel.id == obrigacao_id).first()
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")

    # Atualiza os campos
    db_obrigacao.nome = obrigacao.nome
    db_obrigacao.periodicidade = obrigacao.periodicidade
    db_obrigacao.empresa_id = obrigacao.empresa_id

    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao


# Deletar uma Obrigação Acessória

# Excluir obrigacao http://127.0.0.1:8080/obrigacoes/{ID}
@app.delete("/obrigacoes/{obrigacao_id}", response_model=dict, summary="Excluir obrigação", description="Remove uma obrigação acessória do banco de dados.")
def delete_obrigacao(obrigacao_id: int, db: Session = Depends(get_db)):
    """Apaga uma obrigação acessória pelo ID."""
    db_obrigacao = db.query(ObrigacaoAcessoriaModel).filter(ObrigacaoAcessoriaModel.id == obrigacao_id).first()
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")

    db.delete(db_obrigacao)
    db.commit()
    return {"message": "Obrigação deletada com sucesso"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)

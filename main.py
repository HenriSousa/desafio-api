from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from empresaModel import Empresa
from obrigacaoAssessoriaModel import ObrigacaoAssessoria
from pydanticModel import EmpresaCreate, Empresa, ObrigacaoAssessoriaCreate, ObrigacaoAssessoria

# Criação das tabelas
from empresaModel import Base
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD de Empresa
@app.post("/empresas/", response_model=Empresa)
def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = Empresa(nome=empresa.nome, cnpj=empresa.cnpj, endereco=empresa.endereco, email=empresa.email, telefone=empresa.telefone)
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.get("/empresas/{empresa_id}", response_model=Empresa)
def get_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return db_empresa

# CRUD de ObrigacaoAssessoria
@app.post("/obrigacoes/", response_model=ObrigacaoAssessoria)
def create_obrigacao(obrigacao: ObrigacaoAssessoriaCreate, db: Session = Depends(get_db)):
    db_obrigacao = ObrigacaoAssessoria(nome=obrigacao.nome, periodicidade=obrigacao.periodicidade, empresa_id=obrigacao.empresa_id)
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

@app.get("/obrigacoes/{obrigacao_id}", response_model=ObrigacaoAssessoria)
def get_obrigacao(obrigacao_id: int, db: Session = Depends(get_db)):
    db_obrigacao = db.query(ObrigacaoAssessoria).filter(ObrigacaoAssessoria.id == obrigacao_id).first()
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação Assessória não encontrada")
    return db_obrigacao

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)

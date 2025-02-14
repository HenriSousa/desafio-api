from pydantic import BaseModel
from typing import List
class EmpresaCreate(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: str
    telefone: str

class Empresa(EmpresaCreate):
    id: int

    class Config:
        from_attributes = True

class ObrigacaoAcessoriaCreate(BaseModel):
    nome: str
    periodicidade: str
    empresa_id: int

class ObrigacaoAcessoria(ObrigacaoAcessoriaCreate):
    id: int

    class Config:
        from_attributes = True

class ObrigacaoAcessoriaBase(BaseModel):
    id: int
    nome: str
    periodicidade: str

    class Config:
        from_attributes = True

class EmpresaComObrigacoes(Empresa):
    obrigacoes: List[ObrigacaoAcessoriaBase] = []
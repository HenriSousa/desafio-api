from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Empresa(Base):
    __tablename__ = 'empresas'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, index=True)
    cnpj = Column(String, unique=True, index=True)
    endereco = Column(String)
    email = Column(String, unique=True, index=True)
    telefone = Column(String)

    obrigacoes = relationship("ObrigacaoAcessoria", back_populates="empresa")

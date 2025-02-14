from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ObrigacaoAcessoria(Base):
    __tablename__ = 'obrigacoes_acessorias'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    periodicidade = Column(String)  # mensal, trimestral, anual
    empresa_id = Column(Integer, ForeignKey('empresas.id'))

    empresa = relationship("Empresa", back_populates="obrigacoes")

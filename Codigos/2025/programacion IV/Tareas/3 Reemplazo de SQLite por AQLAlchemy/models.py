from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

class EstadoLectura(enum.Enum):
    leido = "leído"
    no_leido = "no leído"

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    autor = Column(String(100), nullable=False)
    genero = Column(String(50), nullable=False)
    estado_lectura = Column(Enum(EstadoLectura), nullable=False)

from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from utils.positions import Position
from utils.states import States
from database import Base


class Jugador(Base):
    __tablename__ = 'jugadores'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    numero = Column(Integer, nullable=True, unique=True)
    posicion = Column(String, index=True)  # Usar como string ya que 'Position' es un enum
    estado = Column(String, index=True)    # Usar como string ya que 'States' es un enum
    edad = Column(Integer, nullable=True)

    estadisticas = relationship("Estadistica", back_populates="jugador")

    def __repr__(self):
        return f"<Jugador(id={self.id}, nombre={self.nombre}, numero={self.numero})>"


class Estadistica(Base):
    __tablename__ = 'estadisticas'

    id = Column(Integer, primary_key=True, index=True)
    goles = Column(Integer, default=0)
    asistencias = Column(Integer, default=0)
    minutos = Column(Integer, default=0)
    tarjetas_amarillas = Column(Integer, default=0)
    tarjetas_rojas = Column(Integer, default=0)
    partidos_jugados = Column(Integer, default=0)

    jugador_id = Column(Integer, ForeignKey('jugadores.id'))

    jugador = relationship("Jugador", back_populates="estadisticas")

    def __repr__(self):
        return f"<Estadistica(id={self.id}, jugador_id={self.jugador_id})>"
    



class Partido():
    pass


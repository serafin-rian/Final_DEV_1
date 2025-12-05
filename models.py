from pydantic import BaseModel, Field
from typing import Optional
from utils.positions import Position
from utils.states import States

# ============================================
# MODELO JUGADOR
# ============================================

class Jugador(BaseModel):
    """
    Modelo que representa a un jugador del equipo.
    Se usa BaseModel de Pydantic para validar automáticamente los datos.
    """
    id: int
    nombre: str
    numero: Optional[int] = Field(default=None)   # Número de camiseta (opcional)
    posicion: Position                            # Valor del Enum Position
    estado: States                                # Valor del Enum States
    edad: Optional[int] = None



class Estadistica(BaseModel):
    
    tiempo_jugado : int 
    goles : int
    faltas : int
    tarjetas : int



class Partido():
    pass


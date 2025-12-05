from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from models import Jugador, Estadistica
from database import get_db
from utils.positions import Position
from utils.states import States

app = FastAPI(title="sigmotoa FC")

# -----------------------------
# CREAR JUGADOR
# -----------------------------
@app.post("/jugadores", status_code=201)
async def crear_jugador(jugador: Jugador, db: Session = Depends(get_db)):
    # VALIDAR número único (si viene definido)
    if jugador.numero is not None:
        db_jugador = db.query(Jugador).filter(Jugador.numero == jugador.numero).first()
        if db_jugador:
            raise HTTPException(status_code=400, detail="El número de camiseta ya está en uso.")
    
    db.add(jugador)
    db.commit()
    db.refresh(jugador)
    return jugador


# -----------------------------
# LISTAR TODOS LOS JUGADORES
# -----------------------------
@app.get("/jugadores", response_model=List[Jugador])
async def listar_jugadores(db: Session = Depends(get_db)):
    return db.query(Jugador).all()


# -----------------------------
# OBTENER JUGADOR POR ID
# -----------------------------
@app.get("/jugadores/{jugador_id}", response_model=Jugador)
async def obtener_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = db.query(Jugador).filter(Jugador.id == jugador_id).first()
    if jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador


# -----------------------------
# ACTUALIZAR JUGADOR (PUT)
# -----------------------------
@app.put("/jugadores/{jugador_id}", response_model=Jugador)
async def actualizar_jugador(jugador_id: int, datos: Jugador, db: Session = Depends(get_db)):
    jugador = db.query(Jugador).filter(Jugador.id == jugador_id).first()
    if jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    if datos.numero is not None:
        db_jugador = db.query(Jugador).filter(Jugador.numero == datos.numero).first()
        if db_jugador and db_jugador.id != jugador_id:
            raise HTTPException(status_code=400, detail="El número de camiseta ya está en uso.")

    jugador.nombre = datos.nombre
    jugador.numero = datos.numero
    jugador.posicion = datos.posicion
    jugador.estado = datos.estado
    jugador.edad = datos.edad

    db.commit()
    db.refresh(jugador)
    return jugador


# -----------------------------
# ELIMINAR JUGADOR
# -----------------------------
@app.delete("/jugadores/{jugador_id}")
async def borrar_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = db.query(Jugador).filter(Jugador.id == jugador_id).first()
    if jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    db.delete(jugador)
    db.commit()
    return {"mensaje": "Jugador eliminado", "jugador": jugador}


# -----------------------------
# OBTENER ESTADÍSTICAS DEL JUGADOR
# -----------------------------
@app.get("/jugadores/{jugador_id}/estadisticas/resumen")
async def resumen_estadisticas_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = db.query(Jugador).filter(Jugador.id == jugador_id).first()
    if jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    # Obtener las estadísticas del jugador
    estadisticas = db.query(Estadistica).filter(Estadistica.jugador_id == jugador_id).all()

    if not estadisticas:
        return {
            "jugador_id": jugador_id,
            "partidos_jugados": 0,
            "goles": 0,
            "asistencias": 0,
            "minutos": 0,
            "tarjetas_amarillas": 0,
            "tarjetas_rojas": 0
        }

    goles = sum(e.goles for e in estadisticas)
    asistencias = sum(e.asistencias for e in estadisticas)
    minutos = sum(e.minutos for e in estadisticas)
    amarillas = sum(e.tarjetas_amarillas for e in estadisticas)
    rojas = sum(e.tarjetas_rojas for e in estadisticas)
    partidos = len(estadisticas)

    return {
        "jugador_id": jugador_id,
        "partidos_jugados": partidos,
        "goles": goles,
        "asistencias": asistencias,
        "minutos": minutos,
        "tarjetas_amarillas": amarillas,
        "tarjetas_rojas": rojas
    }

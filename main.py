from fastapi import FastAPI, HTTPException
from typing import List
from models import Jugador, Estadistica
from utils.positions import Position
from utils.states import States

app = FastAPI(title="sigmotoa FC")


jugadores: List[Jugador] = []   # lista donde guardaremos los jugadores

@app.get("/")
async def root():
    return {"message": "sigmotoa FC data el mejor equipo de futbol de Colombia"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Bienvenido a sigmotoa FC {name}"}

# -----------------------------
# CREAR JUGADOR
# -----------------------------
@app.post("/jugadores", status_code=201)
async def crear_jugador(jugador: Jugador):
    # VALIDAR numero único (si viene definido)
    if jugador.numero is not None:
        for j in jugadores:
            if j.numero == jugador.numero:
                raise HTTPException(
                    status_code=400,
                    detail="El número de camiseta ya está en uso."
                )
    
    # VALIDAR que el ID no exista
    for j in jugadores:
        if j.id == jugador.id:
            raise HTTPException(
                status_code=400,
                detail="El ID del jugador ya existe."
            )

    jugadores.append(jugador)
    return jugador


# -----------------------------
# LISTAR TODOS LOS JUGADORES
# -----------------------------
@app.get("/jugadores")
async def listar_jugadores():
    return jugadores


# -----------------------------
# OBTENER JUGADOR POR ID
# -----------------------------
@app.get("/jugadores/{jugador_id}")
async def obtener_jugador(jugador_id: int):
    for j in jugadores:
        if j.id == jugador_id:
            return j
    raise HTTPException(status_code=404, detail="Jugador no encontrado")


# -----------------------------
# ACTUALIZAR JUGADOR (PUT)
# -----------------------------
@app.put("/jugadores/{jugador_id}")
async def actualizar_jugador(jugador_id: int, datos: Jugador):
    for i, j in enumerate(jugadores):
        if j.id == jugador_id:

            # VALIDAR número único
            if datos.numero is not None:
                for otro in jugadores:
                    if otro.numero == datos.numero and otro.id != jugador_id:
                        raise HTTPException(
                            status_code=400,
                            detail="El número de camiseta ya está en uso."
                        )

            jugadores[i] = datos
            return datos

    raise HTTPException(status_code=404, detail="Jugador no encontrado")


# -----------------------------
# BORRAR JUGADOR
# -----------------------------
@app.delete("/jugadores/{jugador_id}")
async def borrar_jugador(jugador_id: int):
    for i, j in enumerate(jugadores):
        if j.id == jugador_id:
            eliminado = jugadores.pop(i)
            return {"mensaje": "Jugador eliminado", "jugador": eliminado}

    raise HTTPException(status_code=404, detail="Jugador no encontrado")

# -----------------------------
# estadisticas de un jugador 
# -----------------------------

@app.get("/jugadores/{jugador_id}/estadisticas/resumen")
async def resumen_estadisticas_jugador(jugador_id: int, estadisticas: Estadistica):
    """
    Devuelve un resumen con estadísticas acumuladas del jugador:
    - goles totales
    - asistencias totales
    - minutos jugados
    - tarjetas amarillas
    - tarjetas rojas
    - cantidad de partidos jugados
    """

    # Verificar si el jugador existe
    jugador = None
    for j in jugadores:
        if j.id == jugador_id:
            jugador = j
            break

    if jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    # Filtrar estadísticas del jugador
    stats_jugador = [e for e in estadisticas if e.jugador_id == jugador_id]

    # Si no tiene estadísticas, devolver valores en cero
    if not stats_jugador:
        return {
            "jugador_id": jugador_id,
            "partidos_jugados": 0,
            "goles": 0,
            "asistencias": 0,
            "minutos": 0,
            "tarjetas_amarillas": 0,
            "tarjetas_rojas": 0
        }

    # Sumar estadísticas
    goles = sum(e.goles for e in stats_jugador)
    asistencias = sum(e.asistencias for e in stats_jugador)
    minutos = sum(e.minutos for e in stats_jugador)
    amarillas = sum(e.tarjetas_amarillas for e in stats_jugador)
    rojas = sum(e.tarjetas_rojas for e in stats_jugador)
    partidos = len(stats_jugador)

    # Retornar resumen
    return {
        "jugador_id": jugador_id,
        "partidos_jugados": partidos,
        "goles": goles,
        "asistencias": asistencias,
        "minutos": minutos,
        "tarjetas_amarillas": amarillas,
        "tarjetas_rojas": rojas
    }
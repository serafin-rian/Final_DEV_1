from fastapi import FastAPI, HTTPException
from typing import List
from models import Jugador
from utils.positions import Position
from utils.states import States

app = FastAPI(title="sigmotoa FC")


jugadores: List[Jugador] = []   # lista donde guardaremos los jugadores

@app.get("/")
async def root():
    return {"message": "sigmotoa FC data"}


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

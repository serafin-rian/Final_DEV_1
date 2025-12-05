from fastapi import FastAPI

app = FastAPI(title="sigmotoa FC")


@app.get("/")
async def root():
    return {"message": "sigmotoa FC data el mejor equipo de futbol de Colombia"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Bienvenido a sigmotoa FC {name}"}

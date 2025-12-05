# Sigmotoa FC - FastAPI

Este es un proyecto de API RESTful para el equipo de fútbol "Sigmotoa FC" implementado con **FastAPI** y **SQLAlchemy**. Proporciona varias rutas para gestionar jugadores y estadísticas, así como interactuar con una base de datos SQLite.

## Requisitos

- Python 3.8+
- FastAPI
- Uvicorn (para ejecución del servidor)
- SQLAlchemy (si usas base de datos)
- SQLite (si usas base de datos SQLite)
.
├── main.py          # Archivo principal de FastAPI
├── models.py        # Definición de los modelos (SQLAlchemy)
├── database.py      # Conexión y configuración de la base de datos
├── requirements.txt # Dependencias del proyecto
└── README.md        # Este archivo


uvicorn main:app --reload

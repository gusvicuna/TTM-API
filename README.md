---
title: 
description: 
tags:
  - fastapi
  - python
---

# TrainTextMatch FastAPI

## Running Local
Para correr el programa se debe:

1. Instalar Python >3.8
2. Crear un ambiente virtual con `python -m venv venv`
2. Activar el ambiente virtual con el comando `venv\Scripts\Activate.ps1` (En Powershell) o `venv/bin/activate` (En Bash shell)
3. Instalar paquetes con el comando `make`
4. Correr el comando `python main.py`

Para correr el proyecto como API

1. Asegurar instalacion de paquetes *fastapi* y *uvicorn[standard]* (El comando make debería instalar estos paquetes)
2. Abrir terminal y correr el comando `uvicorn main:app --reload`
3. Abrir el puerto que aparece

Para correrlo con Docker

1. Crear la imagen localmente `docker build . -t chilean-carplates-api`
2. Correr la imagen como contenedor: `docker run --p 8000:80 chilean-carplates-api`

## Recommended
- Abrir el siguiente url para ver documentacion: `http://127.0.0.1:8000/docs`, el path `docs` lleva directamente a una documentacion en OpenAPI

#    API on broser

from fastapi import FastAPI, HTTPException
import httpx
import pandas as pd

app = FastAPI()

@app.get("/characters")
async def get_characters():
    url = "https://rickandmortyapi.com/api/character"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Verifica si la solicitud fue exitosa
            return response.json()      # Devuelve la respuesta como JSON
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al conectar con la API")
    

## execel document:


@app.get("/export-characters")
async def export_characters():
    url = "https://rickandmortyapi.com/api/character"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

        # Procesar los datos de los personajes
        characters = data["results"]
        df = pd.DataFrame(characters)  # Convertir a DataFrame de pandas

        # Seleccionar columnas relevantes
        columns_to_export = ["id", "name", "status", "species", "type", "gender"]
        df = df[columns_to_export]

        # Exportar a un archivo Excel
        excel_file = "characters.xlsx"
        df.to_excel(excel_file, index=False)

        return {"message": f"Datos exportados a {excel_file}"}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al conectar con la API o exportar datos")
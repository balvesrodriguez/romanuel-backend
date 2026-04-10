from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def root():
    return {"status": "Romanuel FMS API online"}

@app.get("/dashboard")
def dashboard():
    try:
        # Traigo todas las tablas crudas para debug
        carretas = supabase.table("carretas").select("*").execute().data
        choferes = supabase.table("choferes").select("*").execute().data
        clientes = supabase.table("clientes").select("*").execute().data
        transacciones = supabase.table("transacciones").select("*").execute().data
        categorias = supabase.table("categorias").select("*").execute().data
        tractores = supabase.table("tractores").select("*").execute().data
        viajes = supabase.table("viajes").select("*").execute().data
        config = supabase.table("config_global").select("*").execute().data
        
        # Devuelvo TODO crudo para ver qué hay
        return {
            "debug": True,
            "tablas": {
                "transacciones": transacciones,
                "viajes": viajes,
                "tractores": tractores,
                "carretas": carretas,
                "choferes": choferes,
                "clientes": clientes,
                "categorias": categorias,
                "config": config
            },
            "cantidad_filas": {
                "transacciones": len(transacciones),
                "viajes": len(viajes),
                "tractores": len(tractores),
                "carretas": len(carretas),
                "choferes": len(choferes),
                "clientes": len(clientes)
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/registrar-viaje")
def registrar_viaje(data: dict):
    try:
        data["fecha_creacion"] = datetime.now().isoformat()
        result = supabase.table("viajes").insert(data).execute()
        return {"success": True, "data": result.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/registrar-transaccion")
def registrar_transaccion(data: dict):
    try:
        data["fecha_creacion"] = datetime.now().isoformat()
        result = supabase.table("transacciones").insert(data).execute()
        return {"success": True, "data": result.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/registrar-mantenimiento")
def registrar_mantenimiento(data: dict):
    try:
        data["fecha_creacion"] = datetime.now().isoformat()
        result = supabase.table("mantenimientos").insert(data).execute()
        return {"success": True, "data": result.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

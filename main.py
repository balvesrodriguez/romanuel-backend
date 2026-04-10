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
        # Traigo todas las tablas que necesita tu dashboard
        carretas = supabase.table("carretas").select("*").execute()
        choferes = supabase.table("choferes").select("*").execute()
        clientes = supabase.table("clientes").select("*").execute()
        transacciones = supabase.table("transacciones").select("*").execute()
        categorias = supabase.table("categorias").select("*").execute()
        tractores = supabase.table("tractores").select("*").execute()
        viajes = supabase.table("viajes").select("*").execute()
        config = supabase.table("config_global").select("*").execute()
        
        return {
            "success": True,
            "carretas": carretas.data,
            "choferes": choferes.data,
            "clientes": clientes.data,
            "transacciones": transacciones.data,
            "categorias": categorias.data,
            "tractores": tractores.data,
            "viajes": viajes.data,
            "config": config.data
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/registrar-ingreso")
def registrar_ingreso(data: dict):
    try:
        data["fecha_creacion"] = datetime.now().isoformat()
        data["tipo"] = "ingreso"  # Marco que es ingreso
        result = supabase.table("transacciones").insert(data).execute()
        return {"success": True, "data": result.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/registrar-egreso")
def registrar_egreso(data: dict):
    try:
        data["fecha_creacion"] = datetime.now().isoformat()
        data["tipo"] = "egreso"  # Marco que es egreso
        result = supabase.table("transacciones").insert(data).execute()
        return {"success": True, "data": result.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

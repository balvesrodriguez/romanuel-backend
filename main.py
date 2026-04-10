from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
from datetime import datetime

app = FastAPI()

# Habilitar CORS para que funcione desde script.google.com
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a Supabase usando las variables de Railway
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def root():
    return {"status": "Romanuel FMS API online"}

@app.get("/dashboard")
def dashboard():
    try:
        # Trae los datos iniciales que necesita tu Index.html
        ingresos = supabase.table("ingresos").select("*").execute()
        egresos = supabase.table("egresos").select("*").execute()
        choferes = supabase.table("choferes").select("*").execute()
        clientes = supabase.table("clientes").select("*").execute()
        
        return {
            "ingresos": ingresos.data,
            "egresos": egresos.data,
            "choferes": choferes.data,
            "clientes": clientes.data
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/registrar-ingreso")
def registrar_ingreso(data: dict):
    try:
        data["fecha_creacion"] = datetime.now().isoformat()
        result = supabase.table("ingresos").insert(data).execute()
        return {"status": "ok", "data": result.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/registrar-egreso")
def registrar_egreso(data: dict):
    try:
        data["fecha_creacion"] = datetime.now().isoformat()
        result = supabase.table("egresos").insert(data).execute()
        return {"status": "ok", "data": result.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

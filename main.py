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
        carretas = supabase.table("carretas").select("*").execute().data or []
        choferes = supabase.table("choferes").select("*").execute().data or []
        clientes = supabase.table("clientes").select("*").execute().data or []
        transacciones = supabase.table("transacciones").select("*").execute().data or []
        categorias = supabase.table("categorias").select("*").execute().data or []
        tractores = supabase.table("tractores").select("*").execute().data or []
        viajes = supabase.table("viajes").select("*").execute().data or []
        config = supabase.table("config_global").select("*").execute().data or []

        ingresos = sum(float(t.get("monto", 0)) for t in transacciones if t.get("tipo") == "ingreso")
        gastos = sum(float(t.get("monto", 0)) for t in transacciones if t.get("tipo") == "egreso")

        viajes_recientes = sorted(viajes, key=lambda x: x.get("fecha", ""), reverse=True)[:5]
        viajes_recientes_map = [{
            "id": v.get("id"),
            "cliente": v.get("cliente", ""),
            "origen": v.get("origen", ""),
            "fecha": v.get("fecha", "")
        } for v in viajes_recientes]

        return {
            "success": True,
            "ingresos": ingresos,
            "gastos": gastos,
            "camiones": len(tractores),
            "viajesRecientes": viajes_recientes_map,
            "alertas": [],
            "tractores": [t.get("patente") for t in tractores if t.get("patente")],
            "carretas": [c.get("patente") for c in carretas if c.get("patente")],
            "categorias": [c.get("nombre") for c in categorias if c.get("nombre")],
            "clientes": [c.get("nombre") for c in clientes if c.get("nombre")],
            "choferes": [c.get("nombre") for c in choferes if c.get("nombre")],
            "waAdmin": config[0].get("whatsapp_admin", "") if config else ""
        }
    except Exception as e:
        return {"success": False, "error": str(e), "viajesRecientes": [], "tractores": [], "carretas": [], "categorias": [], "clientes": [], "choferes": []}

@app.post("/registrar-viaje")
def registrar_viaje(data: dict):
    try:
        result = supabase.table("viajes").insert(data).execute()
        return {"success": True, "data": result.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/registrar-transaccion")
def registrar_transaccion(data: dict):
    try:
        result = supabase.table("transacciones").insert(data).execute()
        return {"success": True, "data": result.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/registrar-mantenimiento")
def registrar_mantenimiento(data: dict):
    try:
        result = supabase.table("mantenimientos").insert(data).execute()
        return {"success": True, "data": result.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

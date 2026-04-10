from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os

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
        transacciones = supabase.table("transacciones").select("*").execute().data or []
        viajes = supabase.table("viajes").select("*").order("fecha", desc=True).limit(5).execute().data or []
        tractores = supabase.table("tractores").select("patente").execute().data or []
        carretas = supabase.table("carretas").select("patente").execute().data or []
        choferes = supabase.table("choferes").select("nombre").execute().data or []
        clientes = supabase.table("clientes").select("nombre").execute().data or []
        categorias = supabase.table("categorias").select("nombre").execute().data or []
        config = supabase.table("config_global").select("whatsapp_admin").execute().data or []

        ingresos = sum(float(t.get("monto", 0)) for t in transacciones if t.get("tipo") == "ingreso")
        gastos = sum(float(t.get("monto", 0)) for t in transacciones if t.get("tipo") == "egreso")

        return {
            "success": True,
            "ingresos": ingresos,
            "gastos": gastos,
            "camiones": len(tractores),
            "viajesRecientes": viajes,
            "alertas": [],
            "tractores": [t["patente"] for t in tractores],
            "carretas": [c["patente"] for c in carretas],
            "choferes": [c["nombre"] for c in choferes],
            "clientes": [c["nombre"] for c in clientes],
            "categorias": [c["nombre"] for c in categorias],
            "waAdmin": config[0]["whatsapp_admin"] if config else ""
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

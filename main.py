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
        # Traigo todas las tablas
        carretas = supabase.table("carretas").select("*").execute().data
        choferes = supabase.table("choferes").select("*").execute().data
        clientes = supabase.table("clientes").select("*").execute().data
        transacciones = supabase.table("transacciones").select("*").execute().data
        categorias = supabase.table("categorias").select("*").execute().data
        tractores = supabase.table("tractores").select("*").execute().data
        viajes = supabase.table("viajes").select("*").execute().data
        config = supabase.table("config_global").select("*").execute().data
        
        # Calculo ingresos y gastos sumando transacciones
        ingresos = sum(float(t.get("monto", 0)) for t in transacciones if t.get("tipo") == "ingreso")
        gastos = sum(float(t.get("monto", 0)) for t in transacciones if t.get("tipo") == "egreso")
        
        # Preparo los últimos 5 viajes para el dashboard
        viajes_recientes = sorted(viajes, key=lambda x: x.get("fecha", ""), reverse=True)[:5]
        viajes_recientes_map = [{
            "id": v.get("id"),
            "cliente": v.get("cliente", ""),
            "origen": v.get("origen", ""),
            "fecha": v.get("fecha", "")
        } for v in viajes_recientes]
        
        # Nombres para los datalist
        nombres_tractores = [t.get("patente") for t in tractores if t.get("patente")]
        nombres_carretas = [c.get("patente") for c in carretas if c.get("patente")]
        nombres_categorias = [c.get("nombre") for c in categorias if c.get("nombre")]
        nombres_clientes = [c.get("nombre") for c in clientes if c.get("nombre")]
        nombres_choferes = [c.get("nombre") for c in choferes if c.get("nombre")]
        
        # WhatsApp admin desde config_global
        wa_admin = ""
        if config and len(config) > 0:
            wa_admin = config[0].get("whatsapp_admin", "")
        
        return {
            "success": True,
            "ingresos": ingresos,
            "gastos": gastos,
            "camiones": len(tractores),
            "viajesRecientes": viajes_recientes_map,
            "alertas": [], # Por ahora vacío, después calculamos vencimientos
            "tractores": nombres_tractores,
            "carretas": nombres_carretas,
            "categorias": nombres_categorias,
            "clientes": nombres_clientes,
            "choferes": nombres_choferes,
            "waAdmin": wa_admin
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

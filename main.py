from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os, uuid
from supabase import create_client

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@app.get("/")
def leer_root():
    return {"status": "Romanuel FMS API online"}

@app.get("/dashboard")
def get_datos_iniciales():
    ing = supabase.table("transacciones").select("monto").eq("tipo","Ingreso").execute()
    egr = supabase.table("transacciones").select("monto").eq("tipo","Egreso").execute()
    tractores = supabase.table("tractores").select("id,patente,km_actual,km_proximo_service").execute()
    carretas = supabase.table("carretas").select("patente").execute()
    categorias = supabase.table("categorias").select("nombre").execute()
    clientes = supabase.table("clientes").select("id,nombre").execute()
    choferes = supabase.table("choferes").select("id,nombre").execute()
    
    ingresos = sum([i['monto'] for i in ing.data])
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os, uuid
from supabase import create_client

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@app.get("/")
def leer_root():
    return {"status": "Romanuel FMS API online"}

@app.get("/dashboard")
def get_datos_iniciales():
    ing = supabase.table("transacciones").select("monto").eq("tipo","Ingreso").execute()
    egr = supabase.table("transacciones").select("monto").eq("tipo","Egreso").execute()
    tractores = supabase.table("tractores").select("id,patente,km_actual,km_proximo_service").execute()
    carretas = supabase.table("carretas").select("patente").execute()
    categorias = supabase.table("categorias").select("nombre").execute()
    clientes = supabase.table("clientes").select("id,nombre").execute()
    choferes = supabase.table("choferes").select("id,nombre").execute()
    
    ingresos = sum([i['monto'] for i in ing.data])
    gastos = sum([e['monto'] for e in egr.data])
    
    alertas = []
    for t in tractores.data:
        if t['km_proximo_service'] and t['km_proximo_service'] > 0:
            faltan = t['km_proximo_service'] - t['km_actual']
            if faltan < 1000:
                alertas.append({"tractor": t['patente'], "kmTotal": t['km_actual'], "kmFaltan": faltan})
    
    return {
        "ingresos": ingresos, "gastos": gastos, 
        "camiones": len(tractores.data),
        "tractores": [t['patente'] for t in tractores.data],
        "carretas": [c['patente'] for c in carretas.data],
        "categorias": [c['nombre'] for c in categorias.data],
        "clientes": [c['nombre'] for c in clientes.data],
        "choferes": [c['nombre'] for c in choferes.data],
        "alertas": alertas
    }
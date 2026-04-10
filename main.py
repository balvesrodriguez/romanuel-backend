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
                "categorias": categorias
            },
            "cantidad_filas": {
                "transacciones": len(transacciones),
                "viajes": len(viajes),
                "tractores": len(tractores)
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

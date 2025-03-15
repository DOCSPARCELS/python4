import json

def fase_3_calcolo_peso_tassato(dati, file_servizi_zone, file_servizi):
    """
    Filtra i servizi disponibili in base alla zona e calcola il peso tassato.
    """

    tipo_listino = dati["tipo_listino"]
    zona_riferimento = dati["zona_riferimento"]
    peso_effettivo = dati["peso_totale"]

   
    # Carica i servizi disponibili (da servizi.json)
    try:
        with open(file_servizi, "r", encoding="utf-8") as f:
            servizi_data = json.load(f)
            servizi_disponibili = servizi_data.get("servizi", [])  # Estrai la lista di servizi
    except:
        print("❌ ERRORE: Il file servizi.json non è leggibile o ha un formato errato!")
        return []

    # Carica le zone dei servizi (da servizi_zone.json)
    try:
        with open(file_servizi_zone, "r", encoding="utf-8") as f:
            servizi_zone = json.load(f)
    except:
        print("❌ ERRORE: Il file servizi_zone.json non è leggibile o ha un formato errato!")
        return []

    # print(f"✅ Servizi disponibili (prima del filtro zona): {[s['codice_servizio'] for s in servizi_disponibili]}")

    # Creiamo una mappa per sapere quali servizi sono validi per ogni zona
    servizi_per_zona = {
        s["codice_servizio"]: s["Zone"] for s in servizi_zone
    }

    # Determina se filtrare per EXPORT o IMPORT
    if tipo_listino == "EXPORT":
        servizi_filtrati = [
            s for s in servizi_disponibili
            if not s["import"] and zona_riferimento in servizi_per_zona.get(s["codice_servizio"], [])
        ]
    elif tipo_listino == "IMPORT":
        servizi_filtrati = [
            s for s in servizi_disponibili
            if s["import"] and zona_riferimento in servizi_per_zona.get(s["codice_servizio"], [])
        ]
    else:
        print("❌ ERRORE: Tipo di listino non valido!")
        return []

    # print(f"✅ Servizi validi dopo il filtro zona: {[s['codice_servizio'] for s in servizi_filtrati]}")

    # Calcolo del peso tassato per ogni servizio
    servizi_finali = []
    for servizio in servizi_filtrati:
        coef_vol = servizio.get("coef_vol", 0)
        
        if coef_vol > 0:
            peso_volumetrico_totale = sum(
                (collo["lunghezza"] * collo["larghezza"] * collo["altezza"]) / coef_vol
                for collo in dati["pacchi"]
            )
        else:
            peso_volumetrico_totale = 0  # Se coef_vol è 0, non calcoliamo il peso volumetrico
        
        peso_tassato = max(peso_effettivo, peso_volumetrico_totale)
        
        servizi_finali.append({
            "servizio": servizio["codice_servizio"],
            "peso_tassato": peso_tassato
        })

        # print("DEBUG - Risultato Fase 3:", servizi_finali)

    
    return servizi_finali

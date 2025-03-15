import json
import os

def fase_2_determinazione_zona(dati, file_zone):
    """
    Determina la zona di partenza e destinazione:
    - Se il paese è Italia, usa il CAP per determinare la zona (ZIT1/ZIT2).
    - Se il paese NON è Italia, usa la zona associata al paese.
    """

    if not os.path.exists(file_zone):
        print(f"❌ Errore: Il file {file_zone} non è stato trovato.")
        return "Sconosciuta", "Sconosciuta"

    with open(file_zone, "r", encoding="utf-8") as file:
        zone_data = json.load(file)

    partenza_paese = dati["partenza_paese"].strip().title()
    destinazione_paese = dati["destinazione_paese"].strip().title()
    cap_partenza = dati["partenza_cap"].strip()
    cap_destinazione = dati["destinazione_cap"].strip()

    # print(f"🔍 DEBUG: Chiavi disponibili in zone.json: {list(zone_data.keys())}")
    print(f"🔍 DEBUG: Cerco zona per '{destinazione_paese}'")

    zona_partenza = "Sconosciuta"
    zona_destinazione = "Sconosciuta"

    # ✅ Determinazione zona di partenza (se Italia, usa CAP)
    if partenza_paese.lower() == "italia":
        if "Italia" in zone_data and "zone" in zone_data["Italia"]:
            for zona, info in zone_data["Italia"]["zone"].items():
                for range_cap in info["cap"]:
                    min_cap, max_cap = map(int, range_cap.split("-"))
                    if min_cap <= int(cap_partenza) <= max_cap:
                        zona_partenza = zona
                        break
        else:
            print("❌ ERRORE: Nessuna zona trovata per l'Italia in zone.json!")

    else:
        zona_partenza = zone_data.get(partenza_paese, {}).get("zona", "Sconosciuta")

    # ✅ Determinazione zona di destinazione (se Italia, usa CAP)
    if destinazione_paese.lower() == "italia":
        if "Italia" in zone_data and "zone" in zone_data["Italia"]:
            for zona, info in zone_data["Italia"]["zone"].items():
                for range_cap in info["cap"]:
                    min_cap, max_cap = map(int, range_cap.split("-"))
                    if min_cap <= int(cap_destinazione) <= max_cap:
                        zona_destinazione = zona
                        break
        else:
            print("❌ ERRORE: Nessuna zona trovata per l'Italia in zone.json!")

    else:
        if destinazione_paese in zone_data:
            zona_destinazione = zone_data[destinazione_paese].get("zona", "Sconosciuta")
        else:
            print(f"❌ ERRORE: '{destinazione_paese}' non trovato in zone.json.")
            destinazione_paese_varianti = [
                destinazione_paese.strip(),
                destinazione_paese.upper(),
                destinazione_paese.lower(),
                destinazione_paese.title(),
                " ".join(word.capitalize() for word in destinazione_paese.split())
            ]

            destinazione_paese_corr = next(
                (var for var in destinazione_paese_varianti if var in zone_data),
                None
            )

            if destinazione_paese_corr:
                print(f"🔍 DEBUG: Nome paese corretto dopo verifica -> '{destinazione_paese_corr}'")
                zona_destinazione = zone_data[destinazione_paese_corr].get("zona", "Sconosciuta")
            else:
                print(f"❌ ERRORE: Nessuna variante trovata per '{destinazione_paese}'.")

    return zona_partenza, zona_destinazione  # ✅ Ritorna sempre due valori validi


def carica_mappa_servizi_zone(file_servizi_zone):
    """Carica la mappa codice_servizio → lista di codice_listino dal JSON."""
    if not os.path.exists(file_servizi_zone):
        print(f"❌ ERRORE: Il file {file_servizi_zone} non esiste.")
        return {}

    try:
        with open(file_servizi_zone, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        mappa_servizi = {}

        for servizio in data:
            codice_servizio = servizio["codice_servizio"]
            codice_listino = servizio["codice_listino"]

            if codice_servizio not in mappa_servizi:
                mappa_servizi[codice_servizio] = []
            
            mappa_servizi[codice_servizio].append(codice_listino)

        return mappa_servizi
    
    except json.JSONDecodeError:
        print(f"❌ ERRORE: Il file {file_servizi_zone} non è un JSON valido.")
        return {}


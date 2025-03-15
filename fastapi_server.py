from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import bisect
import logging
import traceback

app = FastAPI()

# Configurazione del logging
logging.basicConfig(
    filename="error.log",  # Nome del file log
    level=logging.INFO,     # Registra INFO, WARNING, ERROR e CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato log
)
# Funzione per registrare errori con più dettagli
def log_error(messaggio):
    logging.error(messaggio)
    logging.error(traceback.format_exc())  # Registra anche il traceback dell'errore



# Abilita CORS per il frontend su Live Server (porta 5500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Permette solo richieste da Live Server
    allow_credentials=True,
    allow_methods=["*"],  # Permette tutti i metodi (GET, POST, ecc.)
    allow_headers=["*"],  # Permette tutti gli header
)

class PreventivoRequest(BaseModel):
    partenza: str
    destinazione: str
    peso: float

# Percorsi file
CARTELLA_LISTINI = "servizi_listini/listini/"

# Funzione per caricare i listini con gestione errori
def carica_listini():
    listini = {"export": {}, "import": {}}
    
    try:
        for file_name in os.listdir(CARTELLA_LISTINI):
            if file_name.endswith(".json"):
                file_path = os.path.join(CARTELLA_LISTINI, file_name)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        dati_listino = json.load(f)
                        if "import" in file_name.lower():
                            listini["import"][dati_listino["servizio_id"]] = dati_listino.get("tariffe", {})
                        else:
                            listini["export"][dati_listino["servizio_id"]] = dati_listino.get("tariffe", {})
                    except json.JSONDecodeError:
                        log_error(f"⚠️ Errore: Il file {file_name} contiene JSON non valido. Controlla la sua sintassi.")
    except FileNotFoundError:
        log_error(f"❌ Errore: La cartella '{CARTELLA_LISTINI}' non esiste. Verifica il percorso.")
    except Exception as e:
        log_error(f"❌ Errore generico nel caricamento dei listini: {e}")

    return listini


# Carichiamo i listini quando avviamo il server
LISTINI = carica_listini()

# Funzione per determinare se la spedizione è Export o Import
def determina_tipo_spedizione(partenza, destinazione):
    if partenza.lower() == "italia":
        return "export"
    elif destinazione.lower() == "italia":
        return "import"
    else:
        return None  # Se né partenza né destinazione sono Italia, non gestiamo il caso
    
# Percorso file zone
FILE_ZONE = "servizi_listini/zone/zone.json"

# Funzione per caricare le zone
def carica_zone():
    with open(FILE_ZONE, "r", encoding="utf-8") as f:
        zone_data = json.load(f)
    return zone_data

ZONE = carica_zone()

# Funzione per trovare la zona corrispondente
def trova_zona(partenza, destinazione, tipo_spedizione):
    partenza = partenza.strip().title()  # Formattiamo il nome del paese
    destinazione = destinazione.strip().title()

    if tipo_spedizione == "export":
        return ZONE.get(destinazione, {}).get("zona", "Zona Non Trovata")
    elif tipo_spedizione == "import":
        return ZONE.get(partenza, {}).get("zona", "Zona Non Trovata")
    return None


# Funzione per trovare la tariffa in base alla zona e al peso (ottimizzata)
def trova_tariffa(tipo_spedizione, zona, peso):
    peso = float(peso)  # Assicuriamoci che il peso sia un numero
    listino = LISTINI.get(tipo_spedizione, {})  # Prendiamo il listino Export o Import

    risultati = []

    for servizio, tariffe in listino.items():
        if zona not in tariffe:
            continue  # Se la zona non è nel listino, saltiamo

        tariffe_zona = tariffe[zona]  # Tariffe disponibili per questa zona
        pesi_disponibili = sorted(float(p) for p in tariffe_zona.keys() if p.replace('.', '', 1).isdigit())

        # Troviamo il peso più vicino al valore richiesto usando ricerca binaria
        idx = bisect.bisect_left(pesi_disponibili, peso)

        if idx < len(pesi_disponibili):
            peso_trovato = pesi_disponibili[idx]
            tariffa_finale = tariffe_zona[str(int(peso_trovato)) if peso_trovato.is_integer() else str(peso_trovato)]["tariffa_finale"]
            risultati.append({"servizio": servizio, "tariffa": tariffa_finale})

    return risultati



# Percorso file servizi
FILE_SERVIZI = "servizi_listini/servizi/servizi.json"

# Funzione per caricare i nomi dei servizi
def carica_servizi():
    with open(FILE_SERVIZI, "r", encoding="utf-8") as f:
        dati_servizi = json.load(f)
    return {servizio["codice_servizio"]: servizio["nome_servizio"] for servizio in dati_servizi["servizi"]}

SERVIZI_NOMI = carica_servizi()

# Funzione per trovare i tempi di consegna per una zona e un paese specifico
def trova_tempo_consegna(destinazione, zona):
    dati_zona = ZONE.get(destinazione, None)  # Cerchiamo i dati specifici per il paese di destinazione

    if not dati_zona or dati_zona.get("zona") != zona:
        return {}

    # Convertiamo i tempi di consegna in stringhe leggibili
    tempi_consegna = {
        chiave.replace("tempi_", "").upper(): str(valore) if isinstance(valore, (str, int, float)) else "N/A"
        for chiave, valore in dati_zona.items() if chiave.startswith("tempi_")
    }

    return tempi_consegna




# Endpoint FastAPI per calcolare il preventivo
@app.post("/calcola_preventivo")
async def calcola_preventivo(request: PreventivoRequest):
    tipo_spedizione = determina_tipo_spedizione(request.partenza, request.destinazione)

    if tipo_spedizione is None:
        return {"errore": "Le spedizioni Estero → Estero contatta assistenza."}

    # Trova la zona
    zona = trova_zona(request.partenza, request.destinazione, tipo_spedizione)

    if zona == "Zona Non Trovata":
        return {"errore": "Zona non trovata per questa spedizione."}
    
    
    # Trova la tariffa per questa zona e peso
    tariffe = trova_tariffa(tipo_spedizione, zona, request.peso)

    if not tariffe:
        return {"errore": "Tariffa non disponibile. Chiama Assistenza."}

    # Recuperiamo i tempi di consegna dal paese di destinazione
    tempi_consegna = trova_tempo_consegna(request.destinazione, zona)

    # Se non ci sono tempi di consegna, impostiamo "Non disponibile" come valore predefinito
    if not tempi_consegna:
        tempi_consegna = {"DEFAULT": "Non disponibile"}

    for tariffa in tariffe:
        codice_servizio = tariffa["servizio"]
        tariffa["servizio"] = SERVIZI_NOMI.get(codice_servizio, codice_servizio)  # Nome del servizio

        # Associa il tempo di consegna corretto per il paese specifico
        chiave_tempo = codice_servizio.upper()
        tempo_consegna = tempi_consegna.get(chiave_tempo, tempi_consegna.get("DEFAULT", "Non disponibile")).strip()

        # Se il tempo è vuoto, mostriamo "Non disponibile"
        tariffa["tempo_consegna"] = tempo_consegna if tempo_consegna else "Tempi non disponibili. Chiama Assistenza."

    # 📌 Il return ora è dentro la funzione!
    return {
        "tipo_spedizione": tipo_spedizione,
        "zona": zona,
        "tariffe": tariffe
    }

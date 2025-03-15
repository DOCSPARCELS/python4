import sys
import os

# Aggiunge la cartella principale al path di Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fornitori.mondospedizioni.bot import ottieni_tariffe_mondospedizioni
from fornitori.mondospedizioni.login import accedi, close_login_popup

# ✅ Simuliamo i dati di una spedizione di documenti
dati_spedizione_docs = {
    "tipologia": "DOCS",
    "partenza_paese": "Italia",
    "partenza_citta": "Milano",
    "partenza_cap": "20123",
    "destinazione_paese": "Francia",
    "destinazione_citta": "Parigi",
    "destinazione_cap": "75001",
    "peso_totale": "0.5"  # Peso in KG
}

# ✅ Simuliamo i dati di una spedizione di pacchi
dati_spedizione_pkg = {
    "tipologia": "PKG",
    "partenza_paese": "Italia",
    "partenza_citta": "Roma",
    "partenza_cap": "00185",
    "destinazione_paese": "Germania",
    "destinazione_citta": "Berlino",
    "destinazione_cap": "10115",
    "pacchi": [
        {"peso": "2", "lunghezza": "30", "larghezza": "20", "altezza": "15"},
        {"peso": "5", "lunghezza": "40", "larghezza": "30", "altezza": "20"}
    ]
}

def test_spedizione(dati, tipologia):
    print(f"\n🔹 Test: Spedizione {tipologia}")
    try:
        offerte = ottieni_tariffe(dati)
        if offerte:
            print(f"✅ Offerte trovate per {tipologia}: {offerte}")
        else:
            print(f"⚠️ Nessuna offerta trovata per {tipologia}.")
    except Exception as e:
        print(f"❌ Errore durante il test {tipologia}: {e}")

# ✅ Eseguiamo i test con gestione errori migliorata
test_spedizione(dati_spedizione_docs, "Documenti")
test_spedizione(dati_spedizione_pkg, "Pacchi")


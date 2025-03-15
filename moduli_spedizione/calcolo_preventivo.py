import json
import os
import sys

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# 📌 Aggiungiamo il percorso della cartella principale al sys.path
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(base_path)

from fornitori.gestione_fornitori import recupera_tariffe
from fase1_spedizione import raccogli_dati_spedizione
from fase2_determinazione_zona import fase_2_determinazione_zona, carica_mappa_servizi_zone

from fase3_calcolo_peso import fase_3_calcolo_peso_tassato
from fase4_calcolo_tariffa import calcolo_tariffa


edge_options = Options()
# edge_options.add_argument("--headless")  # Esegui senza interfaccia grafica
edge_options.add_argument("--disable-gpu")  # Evita problemi su alcune macchine
edge_options.add_argument("--no-sandbox")  # Evita errori su sistemi con restrizioni
edge_options.add_argument("--disable-software-rasterizer")  # Disattiva il rasterizzatore software
edge_options.add_argument("--disable-renderer-accessibility")  # Disattiva funzioni di accessibilità nel renderer
edge_options.add_argument("--disable-dev-shm-usage")  # Evita problemi di memoria su alcune macchine


# ✅ Inizializza il driver con le nuove opzioni
# print("✅ Creazione driver Edge... (verifica se viene chiamato più volte)")
# service = Service()
# driver = webdriver.Edge(service=service, options=edge_options)
# wait = WebDriverWait(driver, 10)
# print("✅ Driver Edge creato con successo.")


print("\n🟢 FASE 1 - Determinazione Spedizione")
dati_spedizione = raccogli_dati_spedizione()

if dati_spedizione is None:
    exit()

# ✅ Creiamo il dizionario con **tutti i dati**, compresi i pacchi
dati_per_bot = {
    "partenza_paese": dati_spedizione["partenza_paese"],
    "partenza_citta": dati_spedizione["partenza_citta"],
    "partenza_cap": dati_spedizione["partenza_cap"],
    "destinazione_paese": dati_spedizione["destinazione_paese"],
    "destinazione_citta": dati_spedizione["destinazione_citta"],
    "destinazione_cap": dati_spedizione["destinazione_cap"],
    "tipologia": dati_spedizione["tipologia"],
    "peso_totale": dati_spedizione["peso_totale"],
    "pacchi": dati_spedizione["pacchi"]  # ✅ RIMESSO PACCHI!
}

print("\n🟢 AVVIO RICHIESTA TARIFFE AI FORNITORI...\n")

# ✅ Chiamata centralizzata a tutti i fornitori (bot + API)
risultati_bot = recupera_tariffe(dati_per_bot)


# ✅ Stampiamo i risultati ottenuti dai fornitori
if risultati_bot:
    print("\n🔹 RISULTATI DELLE TARIFFE RICEVUTE:")

    fornitori_risultati = {}

    for r in risultati_bot:
        fornitore = r["fornitore"]
        if fornitore not in fornitori_risultati:
            fornitori_risultati[fornitore] = []
        
        fornitori_risultati[fornitore].append(r)

    # ✅ Stampiamo i risultati suddivisi per fornitore
    for fornitore, offerte in fornitori_risultati.items():
        print(f"\n📦 {fornitore} - Offerte disponibili:")
        for r in offerte:
            print(f"   💰 {r['prezzo']} → ⏳ {r['tempi']} → 🚚 {r['corriere']} → 📦 {r['servizio']}")

else:
    print("❌ Nessun preventivo trovato dai fornitori disponibili.")

#print("🔍 Il browser resterà aperto per verifica manuale. Procedo con le fasi successive...")
#print("ℹ️ Chiudi manualmente il browser quando hai terminato.")



print("\n🟢 FASE 2 - Determinazione Zona")
file_zone = os.path.join(base_path, "servizi_listini/zone/zone.json")

zona_partenza, zona_destinazione = fase_2_determinazione_zona(dati_spedizione, file_zone)

if zona_partenza is None or zona_destinazione is None:
    exit()

dati_spedizione["zona_partenza"] = zona_partenza
dati_spedizione["zona_destinazione"] = zona_destinazione


print("\n🟢 FASE 3 - Servizi Disponibili e Peso Tassato")

file_servizi = os.path.join(base_path, "servizi_listini/servizi.json")
file_servizi_zone = os.path.join(base_path, "servizi_listini/servizi_zone.json")

# Determiniamo la zona di riferimento in base al tipo di spedizione
zona_riferimento = dati_spedizione["zona_destinazione"] if dati_spedizione["tipo_listino"] == "EXPORT" else dati_spedizione["zona_partenza"]
dati_spedizione["zona_riferimento"] = zona_riferimento  # Aggiungiamo nei dati

# 🟢 Eseguiamo la Fase 3 UNA SOLA VOLTA
servizi_filtrati = fase_3_calcolo_peso_tassato(dati_spedizione, file_servizi_zone, file_servizi)

if not servizi_filtrati:
    print("❌ ERRORE: Nessun servizio disponibile in Fase 3, impossibile calcolare il peso tassato!")
    exit()

# ✅ Rimuove servizi duplicati PRIMA del ciclo
servizi_filtrati_unici = {s["servizio"]: s for s in servizi_filtrati}.values()

# ✅ Carichiamo la mappa codice_servizio → lista di codice_listino
cartella_listini = os.path.join(base_path, "servizi_listini/listini")
file_servizi_zone = os.path.join(base_path, "servizi_listini/servizi_zone.json")
mappa_servizi = carica_mappa_servizi_zone(file_servizi_zone)

tariffe_per_listino = {}

for servizio in servizi_filtrati_unici:
    dati_spedizione["servizio"] = servizio["servizio"]
    dati_spedizione["peso_tassato"] = servizio["peso_tassato"]

    # ✅ Troviamo i listini corrispondenti per il servizio
    lista_listini = mappa_servizi.get(servizio["servizio"], [])
    
    if not lista_listini:
        print(f"❌ Nessun codice_listino trovato per {servizio['servizio']}")
        continue  

    for codice_listino in lista_listini:
        nome_listino = f"{codice_listino.lower()}.json"
        file_listini = os.path.join(cartella_listini, nome_listino)

        if not os.path.exists(file_listini):
            print(f"❌ Listino non trovato per {servizio['servizio']} ({codice_listino}): {file_listini}")
            continue  

        # ✅ Calcolo tariffa UNA SOLA VOLTA per ogni combinazione servizio-listino
        dettagli_tariffa = calcolo_tariffa(dati_spedizione, file_listini, codice_listino)

        if dettagli_tariffa:
            if codice_listino not in tariffe_per_listino:
                tariffe_per_listino[codice_listino] = []
            tariffe_per_listino[codice_listino].append(dettagli_tariffa)

# ✅ Ora stampiamo le tariffe organizzate per listino
print("\n🟢 FASE 4 - Tempi e Costi (Organizzati per Listino)")
for codice_listino, tariffe in tariffe_per_listino.items():
    #print(f"\n📑 Listino: {codice_listino}")
    for dettagli in tariffe:
        print(f"📦 Servizio {dettagli['servizio']} - Peso Tassato {dettagli['peso_tassato']} kg - 💰 Tariffa € {dettagli['tariffa']:.2f} - 📑 Listino: {codice_listino}")




# ✅ Carichiamo la mappa codice_servizio → lista di codice_listino
mappa_servizi = carica_mappa_servizi_zone(file_servizi_zone)

tariffe_calcolate = []

for servizio in servizi_filtrati:
    dati_spedizione["servizio"] = servizio["servizio"]  # Aggiunge il servizio in analisi

    # ✅ Troviamo i codice_listino corrispondenti (lista)
    lista_listini = mappa_servizi.get(servizio["servizio"], [])
    
    if not lista_listini:
        print(f"❌ Nessun codice_listino trovato per {servizio['servizio']}")
        continue  # Passa al prossimo servizio

    migliore_tariffa = None  # Per memorizzare la tariffa più conveniente

    # ✅ Cerchiamo in tutti i listini disponibili per il servizio
    for codice_listino in lista_listini:
        nome_listino = f"{codice_listino.lower()}.json"
        file_listini = os.path.join(cartella_listini, nome_listino)

        if not os.path.exists(file_listini):
            print(f"❌ Listino non trovato per {servizio['servizio']} ({codice_listino}): {file_listini}")
            continue  # Prova il prossimo listino
    
    for servizio in servizi_filtrati:
        dati_spedizione["servizio"] = servizio["servizio"]
        dati_spedizione["peso_tassato"] = servizio["peso_tassato"]  # ✅ Usa il peso corretto per ogni servizio

        #print("DEBUG - Dati spedizione prima di Fase 4:", dati_spedizione)  # Controllo finale
    
        dettagli_tariffa = calcolo_tariffa(dati_spedizione, file_listini, codice_listino)  # ✅ Passa il codice listino

        if dettagli_tariffa:
            # ✅ Se questa tariffa è la più bassa trovata, la memorizziamo
            if migliore_tariffa is None or dettagli_tariffa["tariffa"] < migliore_tariffa["tariffa"]:
                migliore_tariffa = dettagli_tariffa

    if migliore_tariffa:
        tariffe_calcolate.append(migliore_tariffa)

#if tariffe_calcolate:
#   for tariffa in tariffe_calcolate:
#       print(f" - {tariffa['servizio']}: € {tariffa['tariffa']} (Listino: {tariffa['codice_listino']})")
#else:
#   print("❌ Nessuna tariffa trovata.")

# input("🔍 Il browser resterà aperto. Premi INVIO per chiuderlo...")



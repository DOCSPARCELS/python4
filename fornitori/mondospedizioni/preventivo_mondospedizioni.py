import sys
import os
import subprocess

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait

# Aggiunge il path principale per importare correttamente 'fornitori'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fornitori.mondospedizioni.bot import ottieni_tariffe_mondospedizioni
from fornitori.mondospedizioni.login import accedi, close_login_popup

# ✅ Configura il browser per Selenium
options = webdriver.EdgeOptions()
options.add_argument("--log-level=3")  # Nasconde i log fastidiosi
options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service()
service.creationflags = subprocess.CREATE_NO_WINDOW  # Nasconde la finestra CMD

# ✅ Inizializza il driver di Selenium
driver = webdriver.Edge(service=service, options=options)
wait = WebDriverWait(driver, 5)


def chiedi_dati_spedizione():
    """ Chiede all'utente di inserire i dati per la spedizione """
    print("\n🔹 Inserisci i dati per il preventivo di spedizione:")
    
    # Scegli tra DOCUMENTI o PACCHI
    while True:
        tipologia = input("Tipologia (DOCS/PKG): ").strip().upper()
        if tipologia in ["DOCS", "PKG"]:
            break
        print("⚠️ Inserisci solo 'DOCS' o 'PKG'.")

    partenza_paese = input("Paese di partenza: ").strip()
    partenza_citta = input("Città di partenza: ").strip()
    partenza_cap = input("CAP di partenza: ").strip()
    destinazione_paese = input("Paese di destinazione: ").strip()
    destinazione_citta = input("Città di destinazione: ").strip()
    destinazione_cap = input("CAP di destinazione: ").strip()

    # Se la spedizione è per documenti
    if tipologia == "DOCS":
        peso_totale = input("Peso totale (kg): ").strip()
        return {
            "tipologia": "DOCS",
            "partenza_paese": partenza_paese,
            "partenza_citta": partenza_citta,
            "partenza_cap": partenza_cap,
            "destinazione_paese": destinazione_paese,
            "destinazione_citta": destinazione_citta,
            "destinazione_cap": destinazione_cap,
            "peso_totale": peso_totale
        }

    # Se la spedizione è per pacchi
    pacchi = []
    while True:
        try:
            num_pacchi = int(input("Numero di pacchi: "))
            if num_pacchi > 0:
                break
            print("⚠️ Il numero di pacchi deve essere almeno 1.")
        except ValueError:
            print("⚠️ Inserisci un numero valido.")

    for i in range(num_pacchi):
        print(f"\n📦 Inserisci i dettagli del pacco {i+1}:")
        peso = input("Peso (kg): ").strip()
        lunghezza = input("Lunghezza (cm): ").strip()
        larghezza = input("Larghezza (cm): ").strip()
        altezza = input("Altezza (cm): ").strip()
        pacchi.append({"peso": peso, "lunghezza": lunghezza, "larghezza": larghezza, "altezza": altezza})

    return {
        "tipologia": "PKG",
        "partenza_paese": partenza_paese,
        "partenza_citta": partenza_citta,
        "partenza_cap": partenza_cap,
        "destinazione_paese": destinazione_paese,
        "destinazione_citta": destinazione_citta,
        "destinazione_cap": destinazione_cap,
        "pacchi": pacchi
    }

# ✅ Chiedi i dati all'utente
dati_spedizione = chiedi_dati_spedizione()

# ✅ Effettua il login PRIMA di richiedere il preventivo
print("\n🔑 Effettuo il login su Mondospedizioni...")
if accedi(driver, wait):
    print("✅ Login effettuato con successo!")

    # ✅ Dopo il login, avvia il preventivo
    print("\n🔍 Avvio del preventivo con i dati inseriti...")
    offerte = ottieni_tariffe_mondospedizioni(dati_spedizione, driver)
else:
    print("❌ Errore nel login, impossibile continuare.")
    driver.quit()
    exit()


# ✅ Mostra i risultati
if offerte:
    print("\n✅ Offerte trovate:")
    for offerta in offerte:
        print(f"📦 {offerta['corriere']} → 💰 {offerta['prezzo']} → ⏳ {offerta['tempi']}")
else:
    print("⚠️ Nessuna offerta disponibile per i dati inseriti.")

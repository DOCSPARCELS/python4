import sys
import os
import json
import time
import requests
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# 🔹 Aggiunge il percorso principale del progetto per importare i moduli correttamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fornitori.globalservice.login import login_global_service  # ✅ Import corretto

# Carica le variabili dal file .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_KEY = os.getenv("GOOGLE_API_KEY")

print(f"🔍 DEBUG: API Key usata → {API_KEY}")  # 👈 Controllo se la chiave è corretta

# 🔹 Percorso del file province.json
PERCORSO_PROVINCE = "servizi_listini/zone/province_italia.json"

# 🔹 Carica le province da un file JSON
def carica_province():
    try:
        with open(PERCORSO_PROVINCE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data["province"]  # Usa un dizionario per accesso rapido
    except FileNotFoundError:
        print(f"❌ Errore: Il file {PERCORSO_PROVINCE} non è stato trovato!")
        return {}

PROVINCE_ITALIANE = carica_province()

# 🔹 Funzione per trovare la provincia senza usare Google
def trova_provincia(citta):
    return PROVINCE_ITALIANE.get(citta, "Provincia non trovata")

# 🔹 Funzione per inserire dati nei campi
def inserisci_dato(xpath, valore, nome_campo):
    try:
        campo = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script("arguments[0].click();", campo)
        campo.clear()
        campo.send_keys(valore)
        print(f"✅ {nome_campo} inserito: {valore}")
    except TimeoutException:
        print(f"❌ Errore: Il campo {nome_campo} non è stato trovato!")

# 🔹 Effettua il login su Global Service
driver = login_global_service()

if driver is None:
    print("❌ Login fallito. Controlla le credenziali o il reCAPTCHA.")
    exit()

time.sleep(3)

print("✅ DEBUG: Login completato, procedo con il resto del codice...")

# 🔹 Richiesta dati all'utente
nazione_partenza = input("Inserisci la NAZIONE di partenza: ").strip()
citta_partenza = input("Inserisci la CITTÀ di partenza: ").strip()
nazione_destinazione = input("Inserisci la NAZIONE di destinazione: ").strip()
citta_destinazione = input("Inserisci la CITTÀ di destinazione: ").strip()

provincia_partenza = trova_provincia(citta_partenza) if nazione_partenza.lower() == "italia" else ""
provincia_destinazione = trova_provincia(citta_destinazione) if nazione_destinazione.lower() == "italia" else ""

print(f"📌 Città di Partenza: {citta_partenza} ({nazione_partenza}) -> Provincia: {provincia_partenza}")
print(f"📌 Città di Destinazione: {citta_destinazione} ({nazione_destinazione}) -> Provincia: {provincia_destinazione}")

# 🔹 Compila i campi del modulo
inserisci_dato("//input[@name='nazione_partenza']", nazione_partenza, "Nazione di partenza")
inserisci_dato("//input[@name='nazione_destinazione']", nazione_destinazione, "Nazione di destinazione")

if provincia_partenza != "Provincia non trovata":
    inserisci_dato("//input[@name='provincia_partenza']", provincia_partenza, "Provincia di partenza")

# 🔹 Gestione del campo provincia di destinazione
try:
    provincia_dropdown = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//select[@name='provincia_destinazione']"))
    )
    select = Select(provincia_dropdown)
    select.select_by_visible_text(provincia_destinazione)
    print(f"✅ Provincia di destinazione selezionata: {provincia_destinazione}")
except TimeoutException:
    print("❌ Il campo provincia di destinazione non è visibile o non esiste!")

# 🔹 Mantiene il browser aperto per verifica
input("🔍 Premi INVIO per chiudere il browser dopo aver verificato i dati...")
driver.quit()

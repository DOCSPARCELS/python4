import time
import sys
import os

# Aggiunge la cartella principale del progetto al path di Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from fornitori.mondospedizioni.login import accedi  # ✅ Corretto
from fornitori.mondospedizioni.documenti import documenti, genera_url_documenti, estrai_offerte
from fornitori.mondospedizioni.pacchi import pacchi, genera_url_pacchi, estrai_offerte_pacchi


from webdriver_manager.microsoft import EdgeChromiumDriverManager

def ottieni_tariffe_mondospedizioni(dati_spedizione):
    """Recupera le tariffe reali da Mondospedizioni"""
    print("🔍 Avvio del bot Mondospedizioni...")

    # ✅ Inizializza il driver Edge
    service = Service()
    driver = webdriver.Edge(service=service)
    wait = WebDriverWait(driver, 10)

    # ✅ Esegui il login passando il driver e il wait
    accedi(driver, wait)

    # ✅ Generiamo l'URL in base alla tipologia di spedizione
    if dati_spedizione["tipologia"] == "DOCS":
        url = genera_url_documenti(dati_spedizione)
        offerte = estrai_offerte(driver, wait, url)
    else:
        url = genera_url_pacchi(dati_spedizione)
        offerte = estrai_offerte_pacchi(driver, wait, url)

    # ✅ Chiudiamo il browser dopo aver raccolto le offerte
    driver.quit()

    return [
        {
            "prezzo": o["prezzo"],
            "tempi": o["tempi"],
            "servizio": o.get("servizio", "N/D"),
            "corriere": o.get("corriere", "Mondospedizioni"),
            "fornitore": "Mondospedizioni"
        }
        for o in offerte
    ]


def ottieni_tariffe_mondospedizioni(dati_spedizione):
    """Mondospedizioni temporaneamente disattivato per debug"""
    return []
  

def avvia_bot(driver, wait, dati_spedizione):
    """
    Avvia il bot con i dati ricevuti dalla Fase 1, senza chiedere input all'utente.
    """
    print("✅ Bot avviato con il driver esistente")
    try:
        # Apri il sito
        driver.get("https://www.mondospedizioni.com/")

        # Effettua il login
        accedi(driver, wait)

        # Determina il tipo di spedizione (DOCS o PKG)
        scelta = dati_spedizione["tipologia"].lower()

        if scelta == "docs":
            documenti(driver, wait)

            # Genera URL con i dati della spedizione
            url = genera_url_documenti(dati_spedizione)

            print(f"🔍 Apertura URL generato: {url}")
            driver.get(url)

            # Attendere il caricamento della pagina e poi estrarre i dati delle offerte
            risultati = estrai_offerte_documenti(driver, wait)

        elif scelta == "pkg":
            pacchi(driver, wait)

            # Genera URL con i dati della spedizione
            url = genera_url_pacchi(dati_spedizione)

            print(f"🔍 Apertura URL generato: {url}")
            driver.get(url)

            # Attendere il caricamento della pagina e poi estrarre i dati delle offerte
            risultati = estrai_offerte_pacchi(driver, wait)

        else:
            print("⚠️ Errore: Tipologia non valida.")
            return []

        print(f"✅ Risultati BOT: {risultati}")  # DEBUG: Controlliamo cosa c'è in risultati
        return risultati

    except Exception as e:
        import traceback
        print(f"❌ Errore nel BOT: {e}")
        print(traceback.format_exc())  # Mostra l'errore completo con la traccia dello stack


    finally:
        print("🔍 Il browser resterà aperto per verifica manuale. Procedo con le fasi successive...")
        print("ℹ️ Chiudi manualmente il browser quando hai terminato.")

# ✅ La chiamata a `avvia_bot` va spostata nel file che la usa (ad es. calcolo_preventivo.py) e non qui!

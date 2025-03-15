import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def documenti(driver, wait):
    """
    Naviga alla sezione 'Documenti' dopo il login.
    """
    try:
        print("🔍 Cerco il pulsante 'Documenti'...")
        documenti_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Documenti')]")))
        documenti_button.click()
        print("✅ Sezione 'Documenti' aperta con successo!")

    except Exception as e:
        print(f"❌ Errore nel click su 'Documenti': {e}")

def genera_url_documenti(dati_spedizione):
    """
    Genera l'URL per la spedizione di documenti usando i dati passati dalla Fase 1.
    """
    base_url = "https://www.mondospedizioni.com/search.php"
    
    url = (f"{base_url}?"
           f"nazione_mittente={dati_spedizione['partenza_paese']}"
           f"&loc_mittente={dati_spedizione['partenza_citta']}"
           f"&cap_mittente={dati_spedizione['partenza_cap']}"
           f"&nazione_destinatario={dati_spedizione['destinazione_paese']}"
           f"&loc_destinatario={dati_spedizione['destinazione_citta']}"
           f"&cap_destinatario={dati_spedizione['destinazione_cap']}"
           f"&tipo=docs"
           f"&peso_doc={dati_spedizione['peso_totale']}")

    return url
    print(f"🔗 URL generato per la ricerca: {url}")  # Debug



def estrai_offerte(driver, wait):
    """
    Estrae le offerte di spedizione dalla pagina e le restituisce come lista di dizionari.
    """
    risultati = []  # Lista per salvare le offerte

    time.sleep(5)  # Attende il caricamento della pagina prima di estrarre le offerte

    try:
        # Trova tutti i nomi dei corrieri
        nomi_corrieri = wait.until(lambda driver: driver.find_elements(By.XPATH, "/html/body/section[2]/div/div/div//div[1]/div/a[2]/span"))
        prezzi_corrieri = wait.until(lambda driver: driver.find_elements(By.XPATH, "/html/body/section[2]/div/div/div/div[4]/div[3]/span"))
        tempi_consegna_elements = wait.until(lambda driver: driver.find_elements(By.XPATH, "/html/body/section[2]/div/div/div/div[2]/div/ul/li[3]/a"))

        # Creiamo una lista per i tempi di consegna
        tempi_consegna = []
        for i in range(len(nomi_corrieri)):
            try:
                tempo = tempi_consegna_elements[i].text.strip()
                tempi_consegna.append(tempo)
            except IndexError:
                tempi_consegna.append("N/D")  # Se il valore manca, mettiamo "N/D"

        # Creiamo la lista dei risultati
        for i in range(len(nomi_corrieri)):
            offerta = {
                "corriere": nomi_corrieri[i].text.strip(),
                "prezzo": prezzi_corrieri[i].text.strip(),
                "tempi": tempi_consegna[i]
            }
            risultati.append(offerta)

        print(f"✅ Offerte Estratte: {risultati}")  # DEBUG: Stampiamo i dati estratti

        time.sleep(5)  # Attende il caricamento della pagina
        print(driver.page_source)  # Debug: Mostra il codice HTML della pagina


    except Exception as e:
        print(f"❌ Errore nell'estrazione delle offerte: {e}")

    return risultati  # ✅ Restituiamo i dati estratti

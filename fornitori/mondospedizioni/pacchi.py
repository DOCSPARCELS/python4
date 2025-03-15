from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def pacchi(driver, wait):
    """
    Naviga alla sezione 'Pacchi' dopo il login.
    """
    try:
        print("🔍 Cerco il pulsante 'Pacchi'...")
        pacchi_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Pacchi')]")))
        pacchi_button.click()
        print("✅ Sezione 'Pacchi' aperta con successo!")
    except Exception as e:
        print(f"❌ Errore nel click su 'Pacchi': {e}")

def genera_url_pacchi(dati_spedizione):
    """
    Genera l'URL per la spedizione di pacchi usando i dati passati dalla Fase 1.
    """
    base_url = "https://www.mondospedizioni.com/search.php"

    # Verifica se ci sono pacchi e ottieni il numero
    pacchi = dati_spedizione.get("pacchi", [])
    n_pacchi = len(pacchi)

    if n_pacchi == 0:
        print("❌ Errore: Nessun pacco trovato nei dati della spedizione.")
        return None

    pacchiugualisino = "1" if n_pacchi == 1 else "0"

    # Costruiamo la stringa dei pacchi
    pacchi_params = []
    for i, collo in enumerate(pacchi, start=1):
        pacchi_params.append(f"peso{i}={collo['peso']}&l{i}={collo['lunghezza']}&p{i}={collo['larghezza']}&h{i}={collo['altezza']}")

    pacchi_query = "&".join(pacchi_params)

    # Genera URL dinamico conforme al sito
    url = (f"{base_url}?"
           f"nazione_mittente={dati_spedizione['partenza_paese']}"
           f"&loc_mittente={dati_spedizione['partenza_citta']}"
           f"&cap_mittente={dati_spedizione['partenza_cap']}"
           f"&nazione_destinatario={dati_spedizione['destinazione_paese']}"
           f"&loc_destinatario={dati_spedizione['destinazione_citta']}"
           f"&cap_destinatario={dati_spedizione['destinazione_cap']}"
           f"&tipo=packs&n_pacchi={n_pacchi}&pacchiugualisino={pacchiugualisino}&{pacchi_query}")

    return url



def estrai_offerte_pacchi(driver, wait):
    """
    Estrae le offerte di spedizione pacchi dalla pagina.
    """
    try:
        nomi_corrieri = wait.until(lambda driver: driver.find_elements(By.XPATH, "/html/body/section[2]/div/div/div//div[1]/div/a[2]/span"))
        prezzi_corrieri = wait.until(lambda driver: driver.find_elements(By.XPATH, "/html/body/section[2]/div/div/div/div[4]/div[3]/span"))
        tempi_consegna_elements = wait.until(lambda driver: driver.find_elements(By.XPATH, "/html/body/section[2]/div/div/div/div[2]/div/ul/li[4]/a"))
        
        tempi_consegna = []
        for i in range(len(nomi_corrieri)):
            try:
                tempo = tempi_consegna_elements[i].text.strip()
                tempi_consegna.append(tempo)
            except IndexError:
                tempi_consegna.append("N/D")
        
        for i in range(len(nomi_corrieri)):
            print(f"📦 {nomi_corrieri[i].text} → 💰 {prezzi_corrieri[i].text} → ⏳ {tempi_consegna[i]}")
    except Exception as e:
        print(f"❌ Errore nell'estrazione delle offerte per pacchi: {e}")

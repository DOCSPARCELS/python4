import time
import sys
import os

# Aggiunge la cartella principale al path di ricerca dei moduli
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from google.geocoding import trova_provincia_google
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from fornitori.globalservice.login import login_global_service  # ✅ Usiamo il login di Global Service

# 🔹 Effettua il login su Global Service
driver = login_global_service()

if driver is None:
    print("❌ Login fallito. Controlla le credenziali o il reCAPTCHA.")
    exit()

time.sleep(3)

# 🔹 Chiudere il popup dei cookie
try:
    pulsante_cookie = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/div/div[2]/button[4]")
    pulsante_cookie.click()
    print("✅ Popup cookie chiuso con successo!")
except NoSuchElementException:
    print("⚠️ Nessun popup cookie trovato, procedo normalmente.")

# 🔹 Dati di partenza e destinazione
citta_partenza = "Napoli"
citta_destinazione = "Parigi"

provincia_partenza = trova_provincia_google(citta_partenza, "AIzaSyBvihtyzRMyjD8AGYQ1_DSUEkDrNwcqHjs")
provincia_destinazione = trova_provincia_google(citta_destinazione, "AIzaSyBvihtyzRMyjD8AGYQ1_DSUEkDrNwcqHjs")

print(f"📌 Città di Partenza: {citta_partenza} -> Provincia: {provincia_partenza}")
print(f"📌 Città di Destinazione: {citta_destinazione} -> Provincia: {provincia_destinazione}")

# 🔹 Compila la NAZIONE di partenza solo se il campo è presente e visibile
elementi_nazione_partenza = driver.find_elements(By.XPATH, "/html/body/section[3]/div/div/div/div/div/div/form/div[1]/div[1]/div/input")

if elementi_nazione_partenza:
    campo_nazione_partenza = elementi_nazione_partenza[0]
    is_visible = driver.execute_script("return arguments[0].offsetParent !== null", campo_nazione_partenza)

    if is_visible:
        campo_nazione_partenza.clear()
        campo_nazione_partenza.send_keys("Italia")
        print("✅ Nazione di partenza inserita: Italia")
    else:
        print("⚠️ Il campo nazione di partenza esiste ma è nascosto, non lo tocchiamo.")
else:
    print("⚠️ Il campo nazione di partenza non esiste nel form, ignoriamo l'inserimento.")

# 🔹 Compila la PROVINCIA di partenza
campo_provincia_partenza = driver.find_element(By.XPATH, "/html/body/section[3]/div/div/div/div/div/div/form/div[1]/div[2]/div/input")
campo_provincia_partenza.clear()
campo_provincia_partenza.send_keys(provincia_partenza)

# 🔹 Compila la NAZIONE di destinazione
campo_nazione_destinazione = driver.find_element(By.XPATH, "/html/body/section[3]/div/div/div/div/div/div/form/div[1]/div[3]/div/input")
campo_nazione_destinazione.clear()
nazione_destinazione = "Francia"  # Cambia per testare altre nazioni
campo_nazione_destinazione.send_keys(nazione_destinazione)

time.sleep(1)  # Aspetta il caricamento della pagina

# 🔹 Verifica se la nazione di destinazione è Italia prima di compilare la provincia
if nazione_destinazione.lower() == "italia":
    # Trova il campo provincia (se esiste)
    elementi_provincia = driver.find_elements(By.XPATH, "/html/body/section[3]/div/div/div/div/div/div/form/div[1]/div[4]/div/input")

    if elementi_provincia:  # Se la lista non è vuota, il campo esiste
        campo_provincia_destinazione = elementi_provincia[0]

        # Controlla se il campo è visibile (non nascosto tramite display:none)
        is_visible = driver.execute_script("return arguments[0].offsetParent !== null", campo_provincia_destinazione)

        if is_visible:
            campo_provincia_destinazione.clear()
            campo_provincia_destinazione.send_keys(provincia_destinazione)
            print(f"✅ Provincia di destinazione inserita: {provincia_destinazione}")
        else:
            print("⚠️ Il campo provincia esiste ma è nascosto, non lo tocchiamo.")
    else:
        print("⚠️ Il campo provincia non esiste nel form, ignoriamo l'inserimento.")
else:
    print("✅ Provincia di destinazione non richiesta. Nessuna azione eseguita.")

# 🔹 Seleziona la Tipologia di Spedizione
try:
    campo_tipologia = driver.find_element(By.XPATH, "/html/body/section[3]/div/div/div/div/div/div/form/div[2]/div/div[1]/div/div[1]/div/input")
    campo_tipologia.click()  # 🔹 Clicca sul campo per aprire il menu
    time.sleep(1)

    # 🔹 Seleziona l'opzione "Pacchi"
    opzione_pacchi = driver.find_element(By.XPATH, "//li[contains(text(), 'Pacchi')]")  # Modifica se necessario
    opzione_pacchi.click()

    print("✅ Tipologia di Spedizione selezionata correttamente!")
except Exception as e:
    print(f"❌ Errore nella selezione della Tipologia di Spedizione: {e}")

print(f"✅ Dati inseriti correttamente!")

# 🔹 Attendi qualche secondo per verificare il risultato
time.sleep(5)

# 🔹 Chiudi il browser (togli il commento se vuoi chiuderlo alla fine)
# driver.quit()

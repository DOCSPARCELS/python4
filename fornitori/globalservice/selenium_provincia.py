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

# 🔹 Compila la NAZIONE di partenza
campo_nazione_partenza = driver.find_element(By.XPATH, "/html/body/section[3]/div/div/div/div/div/div/form/div[1]/div[1]/div/input")
campo_nazione_partenza.clear()
campo_nazione_partenza.send_keys("Italia")  

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

# 🔹 Se la nazione è Italia, compila la provincia. Altrimenti NON esegue alcuna azione.
if nazione_destinazione.lower() == "italia":
    try:
        campo_provincia_destinazione = driver.find_element(By.XPATH, "/html/body/section[3]/div/div/div/div/div/div/form/div[1]/div[4]/div/input")
        campo_provincia_destinazione.clear()
        campo_provincia_destinazione.send_keys(provincia_destinazione)
        print(f"✅ Provincia di destinazione inserita: {provincia_destinazione}")
    except Exception:
        print("⚠️ Errore: Il campo provincia non è stato trovato, potrebbe essere un problema con il sito.")
else:
    # 🔹 Qui EVITIAMO completamente di cercare il campo provincia!
    print("✅ Provincia di destinazione non richiesta. Nessun valore inviato.")



# 🔹 Compila la PROVINCIA di destinazione
campo_provincia_destinazione = driver.find_element(By.XPATH, "/html/body/section[3]/div/div/div/div/div/div/form/div[1]/div[4]/div/input")
campo_provincia_destinazione.clear()
campo_provincia_destinazione.send_keys(provincia_destinazione)

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

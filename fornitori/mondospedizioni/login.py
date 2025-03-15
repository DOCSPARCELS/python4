import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Carica credenziali da .env
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def close_cookie_banner(driver, wait):
    """ Chiude il popup dei cookie se presente """
    try:
        print("🔍 Cerco il popup dei cookie...")
        cookie_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "iubenda-cs-accept-btn")))
        cookie_button.click()
        print("✅ Popup cookie chiuso con successo!")
    except Exception:
        print("ℹ️ Nessun popup cookie trovato.")


def accedi(driver, wait):
    """ Esegue il login su Mondospedizioni """
    wait = WebDriverWait(driver, 10)

    print("🌍 Apertura del sito Mondospedizioni...")
    driver.get("https://www.mondospedizioni.com")

    # 📌 Chiudiamo il popup dei cookie prima del login
    close_cookie_banner(driver, wait)

    try:
        # Click su "AREA UTENTI"
        area_utenti_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-login")))
        area_utenti_button.click()

        # Inserisci email e password
        email_field = wait.until(EC.visibility_of_element_located((By.ID, "email_user")))
        email_field.send_keys(EMAIL)

        password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        password_field.send_keys(PASSWORD)

        # Click su "ACCEDI"
        accedi_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//form[@name='loginform']//a[@class='btn btn-submit']")))
        accedi_button.click()

        # 📌 Chiudiamo eventuali popup di conferma login
        close_login_popup(driver)

        # Verifica se il login è avvenuto con successo
        print("🔍 Verifico se l'utente è loggato controllando la navbar...")
        wait.until(EC.presence_of_element_located((By.XPATH, "//nav[contains(@class, 'navbar')]//a[contains(text(), 'Ciao')]")))
        print("✅ Login confermato! L'utente è loggato.")
        return True

    except Exception as e:
        print(f"❌ Errore: Il login non è stato confermato. Dettagli: {e}")
        return False


def close_login_popup(driver):
    """ Chiude eventuali popup di conferma login """
    wait = WebDriverWait(driver, 10)  # Aspetta fino a 10 secondi
    try:
        print("🔍 Cerco il popup di conferma login...")
        
        # Metodo 1: Verifica se esiste un popup di conferma login con JavaScript
        popup_exists = driver.execute_script("return document.querySelector('.swal2-popup button') !== null;")
        
        if popup_exists:
            print("✅ Popup di login rilevato, tentando la chiusura...")
            driver.execute_script("document.querySelector('.swal2-popup button').click();")
            print("✅ Popup chiuso con successo!")
        else:
            print("⚠️ Nessun popup trovato con JavaScript, provo con un altro metodo...")

            # Metodo 2: Trova il popup tramite XPath e chiudilo
            popup_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK') or contains(text(), 'Chiudi')]")))
            popup_button.click()
            print("✅ Popup chiuso con successo tramite XPath!")

    except Exception as e:
        print(f"⚠️ Nessun popup trovato o errore nella chiusura: {e}")



__all__ = ["accedi", "close_login_popup"]

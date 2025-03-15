import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Carica le credenziali dal file .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
EMAIL = os.getenv("GLOBAL_EMAIL")
PASSWORD = os.getenv("GLOBAL_PASSWORD")

# Configura WebDriver per Microsoft Edge
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

# Inizializza il driver di Edge
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=options)

# URL di login
LOGIN_URL = "https://www.globalservicespedizioni.it/login"

def login_global_service():
    print("🔍 Avvio del browser per login...")
    driver.get(LOGIN_URL)
    time.sleep(3)

    # Chiudi il popup dei cookie se presente
    try:
        cookie_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accetta tutti')]")))
        cookie_button.click()
        print("✅ Cookie accettati")
        print("🔄 Scorrimento verso l’alto per visualizzare il form di login...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 4);")
        time.sleep(2)
    except:
        print("⚠️ Nessun popup cookie trovato, continuo...")

    try:
        print("🔍 Cerco il campo EMAIL...")
        email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login[email]")))
        print("✅ Campo EMAIL trovato!")

        print("🔍 Cerco il campo PASSWORD...")
        password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login[password]")))
        print("✅ Campo PASSWORD trovato!")

        print("🔄 Controllo che il form sia completamente visibile...")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", email_input)
        time.sleep(2)

        print("🔍 Cerco il pulsante di login...")
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/section[3]/div/div[3]/div/form/div[3]/div/i"))
        )
        print("✅ Pulsante di login trovato!")

        print("🖱️ Clicco sul campo EMAIL...")
        driver.execute_script("arguments[0].click();", email_input)
        time.sleep(1)

        print("⌨️ Inserisco l'EMAIL...")
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", email_input, EMAIL)
        time.sleep(2)

        email_valore = driver.execute_script("return arguments[0].value;", email_input)
        print(f"🔍 Valore email dopo inserimento: {email_valore}")

        print("🖱️ Clicco sul campo PASSWORD...")
        driver.execute_script("arguments[0].click();", password_input)
        time.sleep(1)

        print("⌨️ Inserisco la PASSWORD...")
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", password_input, PASSWORD)
        time.sleep(2)

        password_valore = driver.execute_script("return arguments[0].value;", password_input)
        print(f"🔍 Valore password dopo inserimento: {password_valore}")

        print("🚀 Clicco il pulsante di login...")
        login_button.click()
        time.sleep(5)

    except Exception as e:
        print(f"❌ Errore durante il login: {e}")
        return None

    if "logout" in driver.page_source.lower():
        print("✅ Login riuscito su Global Service!")
        return driver
    else:
        print("❌ Login fallito. Verifica il reCAPTCHA manualmente e riprova.")
        return None

# ESEMPIO DI UTILIZZO
if __name__ == "__main__":
    session = login_global_service()
    input("Premi INVIO per chiudere il browser...")

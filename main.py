from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Credenziali
USERNAME = "xr01.theia@gmail.com"
PASSWORD = "LBFL2hFxFwUTKc5"

# Nome del piano (parametro che vogliamo inserire nell'input finale)
PLAN_NAME = "MyTestPlan"

# URL di login DJI
LOGIN_URL = "https://account.dji.com/login?appId=es310-manage-service-prod-vg&backUrl=https%3A%2F%2Ffh.dji.com&locale=en_US"

# Percorso del ChromeDriver (modifica in base al tuo sistema)
chrome_driver_path = r"drivers/chrome/chromedriver-win64/chromedriver.exe"

# Imposta il servizio per ChromeDriver
service = Service(executable_path=chrome_driver_path)


def main():
    # Avvia il browser
    driver = webdriver.Chrome(service=service)

    # Apre la pagina di login DJI
    driver.get(LOGIN_URL)

    # Attendi qualche secondo (o sostituisci con un WebDriverWait più accurato)
    time.sleep(3)

    # 1) Inserisci la mail
    email_input = driver.find_element(By.NAME, "username")
    email_input.clear()
    email_input.send_keys(USERNAME)

    # 2) Inserisci la password
    password_input = driver.find_element(By.CSS_SELECTOR, "input[aria-label='Password']")
    password_input.clear()
    password_input.send_keys(PASSWORD)

    # 3) Clicca sul pulsante "Log in"
    login_button = driver.find_element(By.CSS_SELECTOR, "button[data-usagetag='login_button']")
    login_button.click()

    # 4) Attendi caricamento post-login
    wait = WebDriverWait(driver, 20)  # timeout di 20 secondi

    # 5) Clicca sull’icona "enter-icon"
    enter_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.project-enter.project-enter-btn span.enter-icon.uranus-icon"))
    )
    enter_button.click()

    # 6) Clicca sul link che ha href="#/plan"
    plan_link = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.menu-item[href='#/plan']"))
    )
    plan_link.click()

    # 7) Attendi qualche secondo per permettere il caricamento della pagina "Plan"
    time.sleep(5)

    # 8) Clicca sul pulsante "Create Plan"
    create_plan_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.uranus-btn.uranus-btn-primary.uranus-btn-lg.uranus-btn-light"))
    )
    create_plan_button.click()

    # 9) Trova il campo di testo (in cui inserire il nome del plan) e inserisci il nome
    #    In base all'HTML fornito, possiamo identificarlo anche per class o per maxlength:
    plan_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input.uranus-form-row.uranus-input.uranus-dark.uranus-form-row[maxlength='50']"))
    )
    plan_input.clear()
    plan_input.send_keys(PLAN_NAME)

    # 10) Attendi 10 secondi per eventuali verifiche successive
    time.sleep(10)

    # Chiudi il browser
    driver.quit()


if __name__ == "__main__":
    main()

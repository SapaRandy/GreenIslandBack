from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .firebase import db
import time

def parse_plant_info(text):
    result = {}
    if not text:
        return result
    # Sépare chaque ligne à partir du caractère de puce ou du retour à la ligne
    lines = [line.strip("• ").strip() for line in text.split('\n') if line.strip()]
    for line in lines:
        if " : " in line:
            key, value = line.split(" : ", 1)
            result[key.strip()] = value.strip()
    return result

def scrap_plant(name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Essaye d'abord le nom complet
        url = f"https://jaime-jardiner.ouest-france.fr/{name}/"
        driver.get(url)
        time.sleep(2)
        xpath = "//h2[contains(text(), 'Type de plante')]/following-sibling::p[1]"
        element = driver.find_element(By.XPATH, xpath)
        texte = element.text.strip()
        return parse_plant_info(texte)
    except Exception as e:
        return None

        return None  # Rien trouvé
    finally:
        driver.quit()

def insert_plant_in_firestore(plant_data):
    plant_name = plant_data.get('plant')
    plant_info = plant_data.get('texte')
    if not plant_name or not plant_info:
        return False
    plant_data = {
        'name': plant_name,
        'data': plant_info
    }
    try:
        doc_ref = db.collection('plants_data').document(plant_name).set(plant_data)
        if doc_ref.get().exist:
            return False
        doc_ref.set(plant_data)
        return True
    except Exception as e:
        return False
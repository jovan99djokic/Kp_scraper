import os
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
from time import sleep
import requests

# Connect to the database
con = sqlite3.connect("Database.db")

# Firefox options for headless mode
firefox_options = Options()
# firefox_options.add_argument('--headless')
driver = webdriver.Firefox(options=firefox_options)

# Define the database table
cursor = con.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Items (
        Opis TEXT,
        Naslov TEXT,
        Cena TEXT,
        Kategorija TEXT
    )
''')
con.commit()

def scrape_page_data(opis, naslov, cena, kategorija):
    Opis = opis.text
    Naslov = naslov.text 
    Cena = cena.text
    Kategorija = kategorija.text

    print("-" * 50)
    print(f"Opis: {Opis}, Naslov: {Naslov}, Cena: {Cena}, Kategorija: {Kategorija}")

    cursor.execute('''
        INSERT INTO Items (Opis, Naslov, Cena, Kategorija)
        VALUES (?, ?, ?, ?)
    ''', (Opis, Naslov, Cena, Kategorija))
    con.commit()

# Main loop to scrape data from multiple pages

driver.get("https://www.kupujemprodajem.com/saleks-alati/svi-oglasi/154185/1")
for _ in range(50):
    sleep(8)

    # Fetch the Oglas elements after loading the page
    Oglas = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "AdItem_name__Knlo6"))
    )

    for index in range(len(Oglas)):
        # Re-fetch the Oglas elements to avoid stale element reference
        Oglas = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "AdItem_name__Knlo6"))
        )
        print(len(Oglas))
        sleep(3)
        driver.execute_script("window.scrollBy(0, 1000);")

        Oglas[index].click()
        
        try:
            sleep(4)
            # Use WebDriverWait to wait for elements to be present
            opis_opis = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "AdViewDescription_descriptionHolder__kOWyx"))
            )
            naslov_naslov = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "AdViewInfo_name__VIhrl"))
            )
            cena_cena = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "AdViewInfo_price__J_NcC"))
            )
            kategorija_kategorija = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[2]/section[1]/div[1]/div/div[1]"))
            )

            scrape_page_data(opis_opis, naslov_naslov, cena_cena, kategorija_kategorija)
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            driver.back()
            
            sleep(3)
            # Wait for the page to load and elements to be available
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "AdItem_name__Knlo6"))

            )
            sleep(4)

    arrow_right_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[2]/section[3]/ul/li[3]/a")
    arrow_right_element.click()

# Close the database connection and webdriver
con.close()
driver.quit()

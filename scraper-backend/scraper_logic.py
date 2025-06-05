from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os

def create_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=chrome_options)
    

def search_google_maps(search_query, industry_sector):
    print(f"\n🧪 Scraping: '{search_query}' | Industry: '{industry_sector}'")

    driver = create_driver()
    
    try:
        driver.get('https://www.google.com/maps')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'searchboxinput')))
        search_box = driver.find_element(By.ID, 'searchboxinput')
        search_box.send_keys(search_query)
        driver.find_element(By.ID, 'searchbox-searchbutton').click()
        time.sleep(5)


        business_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'Nv2PK')]"))
        )

        print(f"✅ Found {len(business_elements)} business blocks")

        business_data = []
        for business in business_elements:
            try:
                name = business.find_element(By.CSS_SELECTOR, '.qBF1Pd.fontHeadlineSmall').text
                website_elements = business.find_elements(By.CSS_SELECTOR, 'a.lcr4fd.S9kvJb')
                website = website_elements[0].get_attribute('href') if website_elements else "No website"
                try:
                    address_element = business.find_element(By.CSS_SELECTOR, 'div.Io6YTe.fontBodyMedium.kR99db.fdkmkc')
                    address = address_element.text
                except:
                    address = "No address"
                phone = business.find_elements(By.CSS_SELECTOR, 'span.UsdlK')
                phone_elements = business.find_elements(By.CSS_SELECTOR, 'span.UsdlK')
                phone = phone_elements[0].text if phone_elements else "No phone"
                business_data.append({
                    "Name": name,
                    "Address": address,
                    "Website": website,
                    "Phone": phone,
                    "Industry": industry_sector
                })
            except Exception as e:
                print(f"⚠️ Skipped a business block due to parsing error: {e}")

        if business_data:
            print("Sample business:", business_data[0])
        else:
            print("No business data extracted.")
        
        return business_data
    finally:
        driver.quit()
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import mysql.connector
import re
import config

# Setup de Selenium
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# WebDriver path
wd_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=wd_service, options=chrome_options)  # Inicia el WebDriver aquí

# DB setup
db = mysql.connector.connect(**config.db_config)
cursor = db.cursor()

#print("Eliminando tabla")
#query = "DROP TABLE IF EXISTS productsHSN CASCADE;"
#cursor.execute(query)
#print("Creando tabla")
#query = "CREATE TABLE productsHSN (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, brand VARCHAR(255) NOT NULL, price DECIMAL(10,2) NOT NULL, quantity FLOAT, measure VARCHAR(100), url VARCHAR(255));"
#cursor.execute(query)


url = f"https://www.hsnstore.com/nutricion-deportiva?p=1"
print(f"Revisando pagina: {url}")
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
products = soup.find_all('li', {'class': 'item last'})

for product in products:
    name = product.find('div', class_= 'col-xs-12 no-gutter product_name_link').text.strip()
    print(f"Extrayendo producto: {name}")
    brand = product.find('div', class_= 'col-xs-12 no-gutter brand_link').text.strip()

    link_tag = product.find('a', class_='product-image')
    if link_tag is not None:
        product_url = link_tag['href']
        print(f"        Busco en producto: {product_url}")
        print("         Utilizando driver existente")
        driver.get(product_url)

        try:
            info_boxes = driver.find_elements(By.CSS_SELECTOR, "div.col-xs-12.no-padding.product-info-detail.row-equal")
            if not info_boxes:
                print("No se pudo encontrar el elemento. Pasando al siguiente producto...")
                continue
            else:
            
                info_box = info_boxes[0]
                price_per_kg_tag = info_box.find_element(By.CSS_SELECTOR, "div.price-per-kg")
                price_text = price_per_kg_tag.find_element(By.TAG_NAME, "span").text.strip()
                price_num = re.sub(r'[^\d,]', '', price_text)
                price_num = price_num.replace(',', '.')
                if price_num:
                    price = float(price_num)
                    print(f"            Producto: {name} cuesta: {price}")
                else:
                    print("El texto extraído no contiene ningún número.")
                    price = 0.0

                if price > 0:
                    query = "INSERT INTO productsHSN (name, brand, price, quantity, measure, url) VALUES (%s, %s, %s, %s, %s, %s)"
                    values = (name, brand, price, 1, "kg", product_url)
                    cursor.execute(query, values)
        except NoSuchElementException:
            print("No se pudo encontrar el elemento. Pasando al siguiente producto...")
db.commit()
cursor.close()
driver.quit()  # Cierra el WebDriver aquí
db.close()

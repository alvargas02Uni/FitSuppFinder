import requests
from bs4 import BeautifulSoup
import mysql.connector
import re
import config  

# ARCHIVO DEFINITIVO PARA EL WEBSCRAPPING DE MYPROTEIN

db = mysql.connector.connect(**config.db_config)  
cursor = db.cursor()

query = "DROP TABLE IF EXISTS productsMyProtein CASCADE;"
cursor.execute(query)

query = "CREATE TABLE productsMyProtein ( id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, brand VARCHAR(255) NOT NULL, flavor VARCHAR(100), price DECIMAL(10,2) NOT NULL, quantity FLOAT, measure VARCHAR(100), url VARCHAR(255));"
cursor.execute(query)

for i in range(1, 3):
    cursor = db.cursor()
    num = str(i)
    url = "https://www.myprotein.es/nutrition/protein.list?pageNumber="+num
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = soup.find_all('li', class_='productListProducts_product')
    for product in products:
        name = product.find('h3', class_='athenaProductBlock_productName').text.strip()
        name = re.sub(r"\s{2,}.*", "", name)  # Limpiar name
        
        brand = "MyProtein"
        quantity = None
        measure = None
        price = None
        
        link_tag = product.find('a', class_='athenaProductBlock_linkImage')
        if link_tag is not None:
            product_url = "https://www.myprotein.es"+link_tag['href']
            product_response = requests.get(product_url)
            product_soup = BeautifulSoup(product_response.content, 'html.parser')

            flavor_options = product_soup.find('select', {'id': re.compile(r'athena-product-variation-dropdown-*')})
            if flavor_options:
                flavors = flavor_options.find_all('option')
                for flavor in flavors:
                    flavor_text = flavor.text.strip()
                    flavor_text = re.sub(r"\s{2,}.*", "", flavor_text)  # Limpiar flavor
                    
                    price_tag = product_soup.find('span', class_='productPrice_schema productPrice_priceAmount')
                    if price_tag is not None:
                        price = float(price_tag.text.strip())

                    cantidad = product_soup.find('button', class_='athenaProductVariations_box default athenaProductVariationsOption')
                    if cantidad is not None:
                        cantidad_texto = cantidad.text.strip()
                        match = re.match(r"(\d+\.?\d*)\s*(\D+)", cantidad_texto)
                        if match:
                            quantity = float(match.group(1))
                            measure = match.group(2).strip()
                            measure = re.sub(r"\s{2,}.*", "", measure)  # Limpiar measure
                        else:
                            print(f"No match for: {cantidad_texto}")  
                    else:
                        print(f"No 'button' found for: {product_url}") 
                        break

                    query = "INSERT INTO productsMyProtein (name, brand, flavor, price, quantity, measure, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    values = (name, brand, flavor_text, price, quantity, measure, product_url)
                    cursor.execute(query, values)
    
    # Guarda los cambios y cierra la conexión a la base de datos
    db.commit()

for i in range(1, 3):
    cursor = db.cursor()
    num = str(i)
    url = "https://www.myprotein.es/nutrition/vitamins-minerals.list?pageNumber="+num
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = soup.find_all('li', class_='productListProducts_product')
    for product in products:
        name = product.find('h3', class_='athenaProductBlock_productName').text.strip()
        name = re.sub(r"\s{2,}.*", "", name)  # Limpiar name
        
        brand = "MyProtein"
        quantity = None
        measure = None
        price = None
        
        link_tag = product.find('a', class_='athenaProductBlock_linkImage')
        if link_tag is not None:
            product_url = "https://www.myprotein.es"+link_tag['href']
            product_response = requests.get(product_url)
            product_soup = BeautifulSoup(product_response.content, 'html.parser')

            flavor_options = product_soup.find('select', {'id': re.compile(r'athena-product-variation-dropdown-*')})
            if flavor_options:
                flavors = flavor_options.find_all('option')
                for flavor in flavors:
                    flavor_text = flavor.text.strip()
                    flavor_text = re.sub(r"\s{2,}.*", "", flavor_text)  # Limpiar flavor
                    
                    price_tag = product_soup.find('span', class_='productPrice_schema productPrice_priceAmount')
                    if price_tag is not None:
                        price = float(price_tag.text.strip())

                    cantidad = product_soup.find('button', class_='athenaProductVariations_box default athenaProductVariationsOption')
                    if cantidad is not None:
                        cantidad_texto = cantidad.text.strip()
                        match = re.match(r"(\d+\.?\d*)\s*(\D+)", cantidad_texto)
                        if match:
                            quantity = float(match.group(1))
                            measure = match.group(2).strip()
                            measure = re.sub(r"\s{2,}.*", "", measure)  # Limpiar measure
                        else:
                            print(f"No match for: {cantidad_texto}")  
                    else:
                        print(f"No 'button' found for: {product_url}") 
                        break

                    query = "INSERT INTO productsMyProtein (name, brand, flavor, price, quantity, measure, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    values = (name, brand, flavor_text, price, quantity, measure, product_url)
                    cursor.execute(query, values)
    
    # Guarda los cambios y cierra la conexión a la base de datos
    db.commit()


for i in range(1, 2):
    cursor = db.cursor()
    num = str(i)
    url = "https://www.myprotein.es/nutrition/amino-acids.list?pageNumber="+num
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = soup.find_all('li', class_='productListProducts_product')
    for product in products:
        name = product.find('h3', class_='athenaProductBlock_productName').text.strip()
        name = re.sub(r"\s{2,}.*", "", name)  # Limpiar name
        
        brand = "MyProtein"
        quantity = None
        measure = None
        price = None
        
        link_tag = product.find('a', class_='athenaProductBlock_linkImage')
        if link_tag is not None:
            product_url = "https://www.myprotein.es"+link_tag['href']
            product_response = requests.get(product_url)
            product_soup = BeautifulSoup(product_response.content, 'html.parser')

            flavor_options = product_soup.find('select', {'id': re.compile(r'athena-product-variation-dropdown-*')})
            if flavor_options:
                flavors = flavor_options.find_all('option')
                for flavor in flavors:
                    flavor_text = flavor.text.strip()
                    flavor_text = re.sub(r"\s{2,}.*", "", flavor_text)  # Limpiar flavor
                    
                    price_tag = product_soup.find('span', class_='productPrice_schema productPrice_priceAmount')
                    if price_tag is not None:
                        price = float(price_tag.text.strip())

                    cantidad = product_soup.find('button', class_='athenaProductVariations_box default athenaProductVariationsOption')
                    if cantidad is not None:
                        cantidad_texto = cantidad.text.strip()
                        match = re.match(r"(\d+\.?\d*)\s*(\D+)", cantidad_texto)
                        if match:
                            quantity = float(match.group(1))
                            measure = match.group(2).strip()
                            measure = re.sub(r"\s{2,}.*", "", measure)  # Limpiar measure
                        else:
                            print(f"No match for: {cantidad_texto}")  
                    else:
                        print(f"No 'button' found for: {product_url}") 
                        break

                    query = "INSERT INTO productsMyProtein (name, brand, flavor, price, quantity, measure, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    values = (name, brand, flavor_text, price, quantity, measure, product_url)
                    cursor.execute(query, values)
    
    # Guarda los cambios y cierra la conexión a la base de datos
    db.commit()


cursor = db.cursor()
url = "https://www.myprotein.es/nutrition/creatine.list"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

products = soup.find_all('li', class_='productListProducts_product')
for product in products:
    name = product.find('h3', class_='athenaProductBlock_productName').text.strip()
    name = re.sub(r"\s{2,}.*", "", name)  # Limpiar name
    
    brand = "MyProtein"
    quantity = None
    measure = None
    price = None
    
    link_tag = product.find('a', class_='athenaProductBlock_linkImage')
    if link_tag is not None:
        product_url = "https://www.myprotein.es"+link_tag['href']
        product_response = requests.get(product_url)
        product_soup = BeautifulSoup(product_response.content, 'html.parser')

        flavor_options = product_soup.find('select', {'id': re.compile(r'athena-product-variation-dropdown-*')})
        if flavor_options:
            flavors = flavor_options.find_all('option')
            for flavor in flavors:
                flavor_text = flavor.text.strip()
                flavor_text = re.sub(r"\s{2,}.*", "", flavor_text)  # Limpiar flavor
                
                price_tag = product_soup.find('span', class_='productPrice_schema productPrice_priceAmount')
                if price_tag is not None:
                    price = float(price_tag.text.strip())

                cantidad = product_soup.find('button', class_='athenaProductVariations_box default athenaProductVariationsOption')
                if cantidad is not None:
                    cantidad_texto = cantidad.text.strip()
                    match = re.match(r"(\d+\.?\d*)\s*(\D+)", cantidad_texto)
                    if match:
                        quantity = float(match.group(1))
                        measure = match.group(2).strip()
                        measure = re.sub(r"\s{2,}.*", "", measure)  # Limpiar measure
                    else:
                        print(f"No match for: {cantidad_texto}")  
                else:
                    print(f"No 'button' found for: {product_url}") 
                    break

                query = "INSERT INTO productsMyProtein (name, brand, flavor, price, quantity, measure, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (name, brand, flavor_text, price, quantity, measure, product_url)
                cursor.execute(query, values)

# Guarda los cambios y cierra la conexión a la base de datos
db.commit()
cursor.close()


db.close()

import mysql.connector
import re
import config
from bs4 import BeautifulSoup
from selenium import webdriver

print("HOLA")
db = mysql.connector.connect(**config.db_config)
cursor = db.cursor()
print("Conectando con la base de datos")
query = "DROP TABLE IF EXISTS productsHSN CASCADE;"
cursor.execute(query)
print("Se borra la tabla si existe")
query = "CREATE TABLE productsHSN ( id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, brand VARCHAR(255) NOT NULL, price DECIMAL(10,2) NOT NULL, quantity FLOAT, measure VARCHAR(100), url VARCHAR(255));"
cursor.execute(query)
print("Se crea la tabla")

# Configurar Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Ejecutar Chrome en modo headless (sin ventana)
driver = webdriver.Chrome("/home/alvargas/Documentos/3ºaño/2ºcuatri/ISI/chromedriver_linux64", options=options)  # Reemplazar con la ubicación de tu controlador ChromeDriver

for i in range(1, 20):
    cursor = db.cursor()
    num = str(i)
    url = "https://www.hsnstore.com/nutricion-deportiva?p=" + num
    print(f"Conectando a la pagina: {url}")

    # Cargar la página con Selenium
    driver.get(url)
    print("Cargando la página con Selenium")

    # Obtener el contenido HTML modificado por JavaScript
    soup = BeautifulSoup(driver.page_source, "html.parser")
    print("Parseando el contenido")

    products = soup.find_all("li", class_="item last")
    print("Se buscan los productos")
    for product in products:
        name = product.find("div", class_="col-xs-12 no-gutter product_name_link").text.strip()
        brand = product.find("div", class_="col-xs-12 no-gutter brand_link").text.strip()

        print(f"Encontrado el producto: {name}")
        quantity = 0
        measure = "na"
        price = 0.0

        select_weights = product.find("select", class_=lambda x: x and re.compile("product_list_|atributo_").search(x))
        if select_weights:
            weights = select_weights.find_all("option")
            if len(weights) >= 3:
                quantity_text = weights[1].text.strip()
            else:
                quantity_text = weights[0].text.strip()
            print(f"La cantidad es: {quantity_text}")
            match = re.match(r"(\d+\.?\d*)\s*(\D+)", quantity_text)
            if match:
                quantity = float(match.group(1))
                measure = match.group(2).strip()
                measure = re.sub(r"\s{2,}.*", "", measure)
        else:
            print(f"No se encontró 'select' con 'Peso' para: {name}")

        price_tag = product.find("div", class_="final-price")
        if price_tag is not None:
            price = price_tag.text.strip()
            price = price.replace("€", "").replace(",", ".")  # Eliminar el símbolo euro
            price = float(price)


        link_tag = product.find("a", class_="product-image")
        print(f"Revisando si tiene link...")
        if link_tag is not None:
            product_url = link_tag["href"]
            print(f"La url del producto es: {product_url}")

        if measure == 'na' or measure == 'x' or measure == ',':
            print(f"Me salto el producto {name}")
        else:
            query = "INSERT INTO productsHSN (name, brand, price, quantity, measure, url) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (name, brand, price, quantity, measure, product_url)
            cursor.execute(query, values)

    # Guardar los cambios y cerrar el cursor
    db.commit()
    cursor.close()

# Cerrar la conexión a la base de datos y el navegador Selenium
db.close()
driver.quit()

import requests
import re
import config
import mysql.connector

# DB setup
db = mysql.connector.connect(**config.db_config)
cursor = db.cursor()

# Variables de configuración
api_endpoint = 'https://api.rainforestapi.com/request'
api_key = '130F25DE7B994795B44FFD43A5AA1498'
product_name = 'Proteína Whey'

# funcion para obtener el número si lo tiene
def obtener_peso_producto(string):
    # Patrón para buscar números seguidos de kg, g, gr o lbs
    patron = r'(\d+(\.\d+)?)\s*(kg|g|gr|lbs)'

    # Buscar la coincidencia en el string
    coincidencia = re.search(patron, string, re.IGNORECASE)

    if coincidencia:
        peso = float(coincidencia.group(1))
        return peso
    else:
        return None


def obtener_peso_unidad(string):
    # Patrón para buscar la unidad de peso
    patron = r'\d+(\.\d+)?\s*(kg|g|gr|lbs)'

    # Buscar la coincidencia en el string
    coincidencia = re.search(patron, string, re.IGNORECASE)

    if coincidencia:
        unidad = coincidencia.group(2)
        return unidad
    else:
        return None


#print("Eliminando tabla")
#query = "DROP TABLE IF EXISTS productsAMAZON CASCADE;"
#cursor.execute(query)
#print("Creando tabla")
#query = "CREATE TABLE productsAMAZON (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, brand VARCHAR(255) NOT NULL, price DECIMAL(10,2) NOT NULL, quantity FLOAT, measure VARCHAR(100), url VARCHAR(255));"
#cursor.execute(query)


# Obtener el token de acceso
token_endpoint = 'https://api.amazon.com/auth/o2/token'
client_id = 'amzn1.application-oa2-client.ec81485424874082a00432e62aa9533c'
client_secret = 'amzn1.oa2-cs.v1.390fbf88c9104df4e5fb738befc21125a3334c3feecd55d2858c6b684884a190'
scope = 'appstore::apps:readwrite'

# Construye el cuerpo de la solicitud de token
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': scope
}

# Envía la solicitud de token
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.post(token_endpoint, data=data, headers=headers)

# Procesa la respuesta del token
if response.status_code == 200:
    token_data = response.json()
    access_token = token_data['access_token']
    expires_in = token_data['expires_in']
    print('Token de acceso:', access_token)
    print('Expira en (segundos):', expires_in)
else:
    print('Error en la solicitud de token:', response.status_code)
    exit()

# Parámetros de la solicitud a la API de Rainforest
headers = {
    'Authorization': f'Bearer {access_token}'
}

params = {
    'api_key': api_key,
    'type': 'search',
    'amazon_domain': 'amazon.es',
    'search_term': product_name,
    'sort_by': 'featured',
    'max_page': '5'
}

# Envía la solicitud a la API de Rainforest con el token de acceso
response = requests.get(api_endpoint, params=params)

# Procesa la respuesta de la API de Rainforest
if response.status_code == 200:
    data = response.json()
    # Accede a los resultados de la búsqueda
    results = data['search_results']
    # Procesa los resultados según tus necesidades
    for result in results:
        if "price" in result:
            if "link" in result['price']:
                nombre_producto = result['title']
                peso_producto = obtener_peso_producto(result['title'])
                unidad_peso = obtener_peso_unidad(result['title'])
                precio = result['price']['value']
                link = result['price']['link']
                print (nombre_producto)
                print (' ')
                
                print (peso_producto)
                print (' ')
                
                print (unidad_peso)
                print (' ')
                
                print (precio)
                print (' ')
                
                print (link)
                print (' ')
                print (' ')
                print (' ')
                print (' ')
                if unidad_peso != "None":
                    query = "INSERT INTO productsAMAZON (name, brand, price, quantity, measure, url) VALUES (%s, %s, %s, %s, %s, %s)"
                    values = (nombre_producto, "Amazon", precio, peso_producto, unidad_peso, link)
                    cursor.execute(query, values)
                    
else:
    print('Error en la solicitud a la API de Rainforest:', response.status_code)

db.commit()
cursor.close()
db.close()
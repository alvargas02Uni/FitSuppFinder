import mysql.connector

config = {
  'host': 'rafadgvc.mysql.database.azure.com',
    'user': 'rafadgvc',
    'password': 'FitSuppFinder1',
    'database': 'FitSuppFinder'
}

# Inicia la conexión
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

#Para productsHSN
queryHSN = "SELECT * FROM productsHSN"
cursor.execute(queryHSN)

with open('productsHSN.txt', 'w') as f:
    for (id, name, brand, price, quantity, measure, url) in cursor:
        f.write(f'{id} \\ {name} \\ {brand} \\ {price} \\ {quantity} \\ {measure} \\ {url}\n')

#Para productsMyProtein
queryMyProtein = "SELECT id, name, brand, price, quantity, measure, url FROM productsMyProtein"
cursor.execute(queryMyProtein)

with open('productsMyProtein.txt', 'w') as f:
    for (id, name, brand, price, quantity, measure, url) in cursor:
        f.write(f'{id} \\ {name} \\ {brand} \\ {price} \\ {quantity} \\ {measure} \\ {url}\n')

#Para productsMyProtein
queryAmazon = "SELECT * FROM productsAmazon"
cursor.execute(queryAmazon)

with open('productsAmazon.txt', 'w') as f:
    for (id, name, brand, price, quantity, measure, url) in cursor:
        f.write(f'{id} \\ {name} \\ {brand} \\ {price} \\ {quantity} \\ {measure} \\ {url}\n')

cursor.close()
cnx.close()

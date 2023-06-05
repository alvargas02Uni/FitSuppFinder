from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def sort_products(products):
    def sort_key(product):
        quantity = product['quantity'] * get_quantity_multiplier(product['measure'])
        ratio = product['price'] / quantity
        return ratio
    
    products.sort(key=sort_key)

def get_quantity_multiplier(measure):
    if measure == 'g':
        return 1
    elif measure == 'mg':
        return 0.001
    elif measure == 'kg':
        return 1000
    elif measure == 'oz':
        return 28.3495
    elif measure == 'lb':
        return 453.592
    else:
        return 1

def read_file(file_name):
    products = []
    with open(file_name, 'r') as f:
        lines = f.readlines()

        for line in lines:
            columns = line.strip().split('\\')
            product = {
                'id': int(columns[0]),
                'name': columns[1],
                'brand': columns[2],
                'price': float(columns[3]),
                'quantity': float(columns[4]),
                'measure': columns[5],
                'url': columns[6],
            }
            products.append(product)

    return products

def consulta(products, query):
    results = []

    for product in products:
        if query.lower() in product['name'].lower():
            results.append(product)

    return results

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    query = request.form.get('query')

    if query:
        results = execute_query(query)
        return render_template('results.html', query=query, results=results)

    return "Ingrese una consulta de búsqueda válida"

def execute_query(query):
    productsHSN = read_file('productsHSN.txt')
    resultsHSN = consulta(productsHSN, query)

    productsMyProtein = read_file('productsMyProtein.txt')
    resultsMyProtein = consulta(productsMyProtein, query)

    productsAmazon = read_file('productsAmazon.txt')
    resultsAmazon = consulta(productsAmazon, query)

    # Combinar los resultados en una lista
    results = resultsHSN + resultsMyProtein + resultsAmazon

    # Ordenar los resultados
    sort_products(results)

    return results

if __name__ == '__main__':
    app.run()

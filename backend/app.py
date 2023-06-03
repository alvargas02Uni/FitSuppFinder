from flask import Flask, render_template
import os

#Directorio de la aplicacion raiz
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app = Flask(__name__, template_folder=os.path.join(APP_ROOT, 'templates'))
app = Flask(__name__, static_folder=os.path.join(APP_ROOT, 'static'))

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
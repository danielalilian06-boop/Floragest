# app.py
# Proyecto FloraGest - Sprint 2: Gestión de Flores (CRUD + Validaciones + Interfaz)
from flask import Flask, render_template
from auth import auth_bp
from flores import flores_bp

app = Flask(__name__)

# Registro de los blueprints (Sprint 1 y Sprint 2)
app.register_blueprint(auth_bp)
app.register_blueprint(flores_bp)

# Página principal
@app.route('/')
def home():
    return render_template('index.html')

# Página del inventario de flores
@app.route('/flores')
def flores_page():
    return render_template('flores.html')

if __name__ == '__main__':
    print("🚀 FloraGest - Sprint 2 corriendo en http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)

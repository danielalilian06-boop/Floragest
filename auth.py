# auth.py
from flask import Blueprint, request, jsonify
import bcrypt, jwt, datetime

auth_bp = Blueprint('auth', __name__)

CLAVE_SECRETA_JWT = "clave_secreta_de_floragest_12345"
ALGORITMO_JWT = "HS256"

def cifrar_contrasena(contra):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(contra.encode('utf-8'), salt).decode('utf-8')

def verificar_contrasena(contra_plana, hash_guardado):
    return bcrypt.checkpw(contra_plana.encode('utf-8'), hash_guardado.encode('utf-8'))

def generar_token(user_id, rol):
    exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    payload = {'user_id': user_id, 'rol': rol, 'exp': exp}
    return jwt.encode(payload, CLAVE_SECRETA_JWT, algorithm=ALGORITMO_JWT)

# Base de datos simulada
HASH_INICIAL = cifrar_contrasena("Admin123")
DB_USUARIOS = {
    "administrador": {"id": 1, "password_hash": HASH_INICIAL, "rol": "admin"}
}
NEXT_USER_ID = 2

@auth_bp.route('/api/register', methods=['POST'])
def register():
    global NEXT_USER_ID
    data = request.get_json()
    user = data.get('username')
    pwd = data.get('password')

    if not user or not pwd:
        return jsonify({"mensaje": "Usuario y contraseña requeridos"}), 400
    if user in DB_USUARIOS:
        return jsonify({"mensaje": "El usuario ya existe"}), 409

    DB_USUARIOS[user] = {
        "id": NEXT_USER_ID,
        "password_hash": cifrar_contrasena(pwd),
        "rol": "personal"
    }
    NEXT_USER_ID += 1
    return jsonify({"mensaje": "Registro exitoso"}), 201

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = data.get('username')
    pwd = data.get('password')
    usuario = DB_USUARIOS.get(user)

    if not usuario or not verificar_contrasena(pwd, usuario['password_hash']):
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    token = generar_token(usuario['id'], usuario['rol'])
    return jsonify({"mensaje": "Login exitoso", "token": token, "rol": usuario['rol']}), 200

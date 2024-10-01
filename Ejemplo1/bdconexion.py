import pyrebase
import firebase_admin
from firebase_admin import credentials

# Inicialización de Firebase Admin
cred = credentials.Certificate('credentials/firebase_credentials.json')
firebase_app = firebase_admin.initialize_app(cred)

# Configuración de Firebase para Pyrebase
firebaseConfig = {
    "apiKey": "AIzaSyAMWEH8giMBJO4vDqhMpYjDUTJZKWHSbSo",
    "authDomain": "drugshelp-a6819.firebaseapp.com",
    "databaseURL": "https://drugshelp-a6819-default-rtdb.firebaseio.com/",
    "storageBucket": "drugshelp-a6819.appspot.com",
}

# Inicializa Pyrebase para autenticación
firebase = pyrebase.initialize_app(firebaseConfig)

# Exportacion de firebase para usarlo en app.py
def get_firebase():
    return firebase

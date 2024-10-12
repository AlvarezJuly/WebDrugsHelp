import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

# Inicialización de Firebase Admin para Firestore 
cred = credentials.Certificate('credentials/firebase_credentials.json')
firebase_app = firebase_admin.initialize_app(cred)
# Inicialización de Firestore
db = firestore.client()

# Configuración de Firebase para Pyrebase (usado para autenticación y Realtime Database)
firebaseConfig = {
    "apiKey": "AIzaSyAMWEH8giMBJO4vDqhMpYjDUTJZKWHSbSo",
    "authDomain": "drugshelp-a6819.firebaseapp.com",
    "databaseURL": "https://drugshelp-a6819-default-rtdb.firebaseio.com/",
    "storageBucket": "drugshelp-a6819.appspot.com",
}

# Inicialización de Pyrebase para autenticación
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()  # Autenticación con Pyrebase

# Exportación de Firebase para usarlo en app.py 
def get_firebase():
    return firebase

# Exportación de Firestore para usarlo en app.py
def get_firestore():
    return db

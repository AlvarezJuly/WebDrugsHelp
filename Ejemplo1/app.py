from flask import Flask, render_template, request, redirect, url_for, flash
import bdconexion

app = Flask(__name__)
app.secret_key = "Julissa2000_DH"  # Para usar flash messages

# Método de conexión
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Acerca')
def acerca():
    return render_template('acercade.html')

@app.route('/QueDefine')
def queDefine():
    return render_template('define.html')

@app.route('/Login', methods=['GET', 'POST'])
def login():
    firebase = bdconexion.get_firebase()  # Obtener la instancia de firebase

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            # Intento de autenticación
            user = firebase.auth().sign_in_with_email_and_password(email, password)
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('panel'))
        except Exception as e:
            # Si ocurre un error
            flash("Credenciales incorrectas. Inténtalo de nuevo.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/Panel')
def panel():
        # Obtener la instancia de Firestore desde bdconexion
    db = bdconexion.get_firestore()  # Obtener la referencia a Firestore

    # Obtener todos los documentos de la colección "contactos"
    contactos_ref = db.collection('contactos')
    especialistas = contactos_ref.stream()  # Para Firestore con firebase_admin, usa .stream()

    # Crear una lista para almacenar los datos de los especialistas
    lista_especialistas = []
    for especialista in especialistas:
        data = especialista.to_dict()  # Convertir los datos a diccionario
        lista_especialistas.append(data)

    # Renderizar la plantilla con la lista de especialistas
    return render_template('panelAdmin.html', especialistas=lista_especialistas)

if __name__ == '__main__':
    app.run(debug=True, port=8080)

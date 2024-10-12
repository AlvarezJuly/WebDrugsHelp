from flask import Flask, render_template, request, redirect, url_for, flash
import bdconexion #archivo que contiene la conxión con firebase

app = Flask(__name__)
app.secret_key = "Julissa2000_DH"  # Para usar flash messages


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
            #Para error
            flash("Credenciales incorrectas. Inténtalo de nuevo.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/Panel')
def panel():
        # Obtener la instancia de Firestore desde bdconexion
    db = bdconexion.get_firestore()  # Obtener la referencia a Firestore

    #colección "contactos"
    contactos_ref = db.collection('contactos')
    especialistas = contactos_ref.stream()  # Para Firestore con firebase_admin, usa .stream()

    #lista para almacenar los datos
    lista_especialistas = []
    for especialista in especialistas:
        data = especialista.to_dict()  # Convertir los datos a lista
        lista_especialistas.append(data)

    return render_template('panelAdmin.html', especialistas=lista_especialistas)

@app.route('/guardar_especialista', methods=['POST'])
def guardar_especialista():
    db = bdconexion.get_firestore()  # Obtener la referencia a Firestore

    # Obtener los datos enviados por el formulario del modal
    nombre = request.form['nombreNuevo']
    correo = request.form['correoNuevo']
    ciudad = request.form['ciudadNueva']
    telefono = request.form['telefonoNuevo']

    #  diccionario con los datos del especialista
    nuevo_especialista = {
        "nombreCom": nombre,
        "correo": correo,
        "ciudad": ciudad,
        "numero": telefono
    }

    try:
        # Agregando el especialista a la colección 'contactos'
        db.collection('contactos').add(nuevo_especialista)
        flash("Especialista agregado con éxito", "success")
    except Exception as e:
        flash(f"Error al agregar el especialista: {e}", "danger")

    # Redirigir de nuevo al panel
    return redirect(url_for('panel'))



if __name__ == '__main__':
    app.run(debug=True, port=8080)

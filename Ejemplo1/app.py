from flask import Flask, render_template, request, redirect, url_for, jsonify
import bdconexion  # archivo que contiene la conexión con Firebase

app = Flask(__name__)

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
    firebase = bdconexion.get_firebase()  #instancia de Firebase

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            # Intento de autenticación
            user = firebase.auth().sign_in_with_email_and_password(email, password)
            print("Inicio de sesión exitoso")  # imprime 
            return redirect(url_for('panel'))
        except Exception as e:
            # Para error
            print("Credenciales incorrectas. Inténtalo de nuevo.")  #Se imprime el error
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/Panel')
def panel():
    #Método Get 
    # Instancia de Firestore desde mi arhivo bdconexion
    db = bdconexion.get_firestore()

    # colección "contactos"
    contactos_ref = db.collection('contactos')
    especialistas = contactos_ref.stream()  # Para Firestore con firebase_admin, usa .stream()

    # lista para almacenar los datos
    lista_especialistas = []
    for especialista in especialistas:
        data = especialista.to_dict()  # Convertir los datos a diccionario
        data['id'] = especialista.id  # Guardar también el ID del documento
        lista_especialistas.append(data)
    return render_template('panelAdmin.html', especialistas=lista_especialistas)

@app.route('/guardar_especialista', methods=['POST'])
def guardar_especialista():
    db = bdconexion.get_firestore()  

    # Obtner los datos del modal
    nombre = request.form['nombreNuevo']
    correo = request.form['correoNuevo']
    ciudad = request.form['ciudadNueva']
    telefono = request.form['telefonoNuevo']

    # Campos del nuevo especialista para enviar a la bd
    nuevo_especialista = {
        "nombreCom": nombre,
        "correo": correo,
        "ciudad": ciudad,
        "numero": telefono
    }

    try:
        # Agregando el especialista a la colección que en la bd es 'contactos'
        #y se muestras las alertas de validación o para atrapar algun error
        db.collection('contactos').add(nuevo_especialista)
        print("Especialista agregado con éxito") 
    except Exception as e:
        print(f"Error al agregar el especialista: {e}")  #error

    return redirect(url_for('panel'))  #panel después de guardar

@app.route('/eliminar/<id>', methods=['DELETE'])
def eliminar_especialista(id):
    db = bdconexion.get_firestore()
    try:
        db.collection('contactos').document(id).delete()
        print("Especialista eliminado con éxito")  # Muestra mensaje de sastifactorio.
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error al eliminar especialista: {e}")  # Imprime el error
        return jsonify({"success": False})

# Ruta para editar especialista
@app.route('/editar/<id>', methods=['PUT'])
def editar_especialista(id):
    db = bdconexion.get_firestore()
    data = request.get_json()  # Recibir datos en formato JSON

    try:
        db.collection('contactos').document(id).update({
            'nombreCom': data['nombre'],
            'correo': data['correo'],
            'ciudad': data['ciudad'],
            'numero': data['telefono']
        })
        print("Especialista editado con éxito")  # Imprime el éxito
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error al editar especialista: {e}")  # Imprime el error
        return jsonify({"success": False})

if __name__ == '__main__':
    app.run(debug=True, port=8080)

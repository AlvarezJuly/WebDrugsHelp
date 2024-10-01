from flask import Flask, render_template, request, redirect, url_for, flash
import bdconexion

app = Flask(__name__)
app.secret_key = "Julissa2000_DH"  # Para usar flash messages

# Método de conexión
@app.route('/')
def Inicio():
    return render_template('index.html')

@app.route('/Acerca')
def Acerca():
    return render_template('acercade.html')

@app.route('/QueDefine')
def QueDefine():
    return render_template('define.html')

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    firebase = bdconexion.get_firebase()  # Obtener la instancia de firebase

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            # Intento de autenticación
            user = firebase.auth().sign_in_with_email_and_password(email, password)
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('Panel'))
        except Exception as e:
            # Si ocurre un error
            flash("Credenciales incorrectas. Inténtalo de nuevo.", "danger")
            return redirect(url_for('Login'))

    return render_template('login.html')

@app.route('/Panel')
def Panel():
    return render_template('panelAdmin.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)

from flask import Flask, render_template

#Coenxion al la base de datos


app = Flask (__name__)

#metod de conexion

@app.route('/')
def Inicio():
    return render_template('index.html')

@app.route('/Acerca')
def Acerca():
    return render_template('acercade.html')

@app.route('/QueDefine')
def QueDefine():
    return render_template('define.html')

@app.route('/Login')
def Login():
    return render_template('login.html')

@app.route('/Panel')
def Panel():
    return render_template('panelAdmin.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
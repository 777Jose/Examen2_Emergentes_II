from flask import Flask, render_template, request, redirect, session, url_for


app = Flask(__name__)
app.secret_key = 'clave_secreta'

def productos():
    if 'productos' not in session:
        session['productos'] = []

def generar_id_unico():
    productos()
    if session['productos']:
        return max([p['id'] for p in session['productos']]) + 1
    else:
        return 1

@app.route('/')
def index():
    productos()
    return render_template('index.html', productos=session['productos'])

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        productos()
        producto = {
            'id': generar_id_unico(),
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }
        session['productos'].append(producto)
        session.modified = True
        return redirect(url_for('index'))
    return render_template('agregar_producto.html')

@app.route('/eliminar/<int:producto_id>')
def eliminar_producto(producto_id):
    productos()
    session['productos'] = [p for p in session['productos'] if p['id'] != producto_id]
    session.modified = True
    return redirect(url_for('index'))

@app.route('/editar/<int:producto_id>', methods=['GET', 'POST'])
def editar_producto(producto_id):
    productos()
    producto = next((p for p in session['productos'] if p['id'] == producto_id), None)
    
    if request.method == 'POST':
        # Actualizar los campos del producto excepto el ID
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))

    return render_template('editar_producto.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Blueprint, render_template, request, redirect, url_for
from app.__init__ import db
from app.blueprints.pedidos.models import Pedido
from app.blueprints.clientes.models import Cliente
from app.blueprints.productos.models import Producto
from datetime import datetime

bp_pedidos = Blueprint("bp_pedidos", __name__, template_folder="templates")


@bp_pedidos.route('/')
def index():
    pedidos = Pedido.query.all()  # estaba Producto.query.all()
    return render_template('pedido/index.html', pedidos=pedidos)


from flask import Blueprint, render_template, request, redirect, url_for, flash # Importamos flash para alertas

@bp_pedidos.route('/create', methods=['GET', 'POST'])
def create():
    clientes = Cliente.query.all()
    productos = Producto.query.all()
    
    if request.method == 'GET':
        return render_template('pedido/create.html', clientes=clientes, productos=productos)
        
    elif request.method == 'POST':
        fecha = datetime.strptime(request.form.get('fecha'), '%Y-%m-%d')
        monto = request.form.get('monto')
        producto_id = int(request.form.get('producto_id'))
        cliente_id = int(request.form.get('cliente_id'))
        
        # 1. Buscar el producto que se está comprando
        producto = Producto.query.get_or_404(producto_id)
        
        # 2. Validar si hay stock disponible (asumiendo que resta 1)
        cantidad_a_restar = 1 
        if producto.stock < cantidad_a_restar:
            # Si no hay stock, mandamos una alerta y recargamos el formulario
            (f"No hay suficiente stock de {producto.nombre}. Stock actual: {producto.stock}", "danger")
            return render_template('pedido/create.html', clientes=clientes, productos=productos)
        # 3. Disminuir el stock del producto
        producto.stock -= cantidad_a_restar
        # 4. Crear el registro del pedido
        pedido = Pedido(
            fecha=fecha, 
            monto=float(monto), 
            producto_id=producto_id, 
            cliente_id=cliente_id
        )
        
        # 5. Guardar todo en la base de datos
        db.session.add(pedido)
        # SQLAlchemy es inteligente: detecta que modificaste 'producto.stock' 
        # y hará el UPDATE del producto y el INSERT del pedido al mismo tiempo
        db.session.commit()
        
        return redirect(url_for('bp_pedidos.index'))


@bp_pedidos.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    pedido = Pedido.query.filter_by(id=id).first_or_404()
    clientes = Cliente.query.all()
    productos = Producto.query.all()
    if request.method == 'GET':
        return render_template('pedido/edit.html', pedido=pedido, clientes=clientes, productos=productos)
    elif request.method == 'POST':
        pedido.fecha = datetime.strptime(request.form.get('fecha'), '%Y-%m-%d')
        pedido.monto = float(request.form.get('monto'))
        pedido.producto_id = int(request.form.get('producto_id'))
        pedido.cliente_id = int(request.form.get('cliente_id'))
        db.session.commit()
        return redirect(url_for('bp_pedidos.index'))


@bp_pedidos.route('/delete/<int:id>')
def delete(id):
    pedido = Pedido.query.filter_by(id=id).first()
    
    db.session.delete(pedido)
    db.session.commit()
    
    return redirect(url_for('bp_pedido.index'))
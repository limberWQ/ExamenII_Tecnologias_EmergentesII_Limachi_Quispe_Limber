from flask import Blueprint, render_template, request, redirect, url_for
from app import db

from app.blueprint.pedidos.models import Pedido
from app.blueprint.clientes.models import Cliente
from app.blueprint.productos.models import Producto

bp_pedidos = Blueprint("bp_pedidos", __name__, template_folder="templates")

@bp_pedidos.route('/')
def index():
    pedidos = Producto.query.all()
    return render_template("index.html", pedidos=pedidos)

#crear
@bp_pedidos.route('/create', methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        clientes = Cliente.query.all()
        productos = Producto.query.all()
        return render_template('pedido/create.html',clientes=clientes, productos=productos)
    elif request.method == 'POST':
        monto = request.form.get('monto')
        producto_id = request.form.get('producto_id')
        cliente_id = request.form.get('cliente_id')
        
        #crear objeto pedidos
        pedido = Pedido(monto=float(monto), producto_id=int(producto_id), cliente_id=int(cliente_id))
        
        #insertar en la bd a traves del ORM
        db.session.add(pedido)
        db.session.commit()
        
        return redirect(url_for('bp_pedidos.index'))
    
#editar
@bp_pedidos.route('/edit/<int:id>', methods =['GET', 'POST'])
def edit(id):
    pedido = Pedido.query.filter_by(id=id).first()
    if request.method == 'GET':
        return redirect(url_for('bp_pedidos.index'))
    elif request.method == 'POST':
        pedido.monto = request.form.get('monto')
        pedido.producto_id = request.form.get('producto_id')
        pedido.cliente_id = request.form.get('cliente_id')
        db.session.commit()
        return redirect(url_for('bp_pedidos.index'))
    
@bp_pedidos.route('/delete/<int:id>')
def delete(id):
    pedido = Pedido.query.filter_by(id=id).first()
    
    db.session.delete(pedido)
    db.session.commit()
    
    return redirect(url_for('bp_pedidos.index'))
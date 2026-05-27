from flask import Blueprint, render_template, request, redirect, url_for
from app.__init__ import db

from app.blueprints.productos.models import Producto

bp_productos = Blueprint("bp_productos", __name__, template_folder="templates")

@bp_productos.route('/')
def index():
    productos = Producto.query.all()
    return render_template('producto/index.html', productos=productos)

#crear
@bp_productos.route('/create', methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('producto/create.html')
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
        
        #crear objeto productos
        producto = Producto(nombre=nombre, precio=precio, stock=stock)
        
        #insertar en la bd a traves del ORM
        db.session.add(producto)
        db.session.commit()
        
        return redirect(url_for('bp_productos.index'))
    
#editar
@bp_productos.route('/edit/<int:id>', methods =['GET', 'POST'])
def edit(id):
    producto = Producto.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('producto/edit.html', producto=producto)
    elif request.method == 'POST':
        producto.nombre = request.form.get('nombre')
        producto.precio = request.form.get('precio')
        producto.stock = request.form.get('stock')
        db.session.commit()
        return redirect(url_for('bp_productos.index'))
    
@bp_productos.route('/delete/<int:id>')
def delete(id):
    producto= Producto.query.filter_by(id=id).first()
    
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('bp_productos.index'))
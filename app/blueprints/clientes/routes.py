from flask import Blueprint, render_template, request, redirect, url_for
from app.__init__ import db

from app.blueprints.clientes.models import Cliente

bp_cliente = Blueprint("bp_cliente", __name__, template_folder="templates")

@bp_cliente.route('/')
def index():
    clientes = Cliente.query.all()
    return render_template('cliente/index.html', clientes=clientes)

#crear
@bp_cliente.route('/create', methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('cliente/create.html')
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        
        #crear objeto cliente
        cliente = Cliente(nombre = nombre, telefono = telefono)
        
        #insertar en la bd a traves del ORM
        db.session.add(cliente)
        db.session.commit()
        
        return redirect(url_for('bp_cliente.index'))
    
#editar
@bp_cliente.route('/edit/<int:id>', methods =['GET', 'POST'])
def edit(id):
    cliente = Cliente.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('cliente/edit.html', cliente=cliente)
    elif request.method == 'POST':
        cliente.nombre = request.form.get('nombre')
        cliente.telefono = request.form.get('telefono')
        db.session.commit()
        return redirect(url_for('bp_cliente.index'))
    
@bp_cliente.route('/delete/<int:id>')
def delete(id):
    cliente = Cliente.query.filter_by(id=id).first()
    
    db.session.delete(cliente)
    db.session.commit()
    
    return redirect(url_for('bp_cliente.index'))
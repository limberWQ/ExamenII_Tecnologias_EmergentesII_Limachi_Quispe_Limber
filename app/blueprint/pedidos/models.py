from app import db
from datetime import datetime

class Pedido(db.Model):
    __tablename__ = "pedidos"
    
    id = db.Column(db.Intenger, primary_key = True)
    fecha = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    monto = db.Column(db.Float, nullable = False)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable = False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable = False)
    

from app.__init__ import db

class Producto(db.Model):
    __tablename__ ="productos"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable = False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable = False)
    
    #Relacion con pedidos
    pedidos = db.relationship("Pedido", backref="producto", lazy=True, cascade="all, delete-orphan")    
    
    def __repr__(self):
        return f"<PRODUCTO: {self.nombre} - {self.precio} - {self.stock}>"
    
    
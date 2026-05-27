from app import db

class Cliente(db.Model):
    __tablename__ ="clientes"
    
    
    id = db.Column(db.Integer, primary_key = True)
    
    nombre = db.Column(db.String(100), nullable = False)
    telefono = db.Column(db.String(20), nullable = False)
    
    # relacion con pedidos
    pedidos = db.relationship("Pedido", backref="cliente", lazy=True, cascade="all, delete-orphan")    
    
    def __repr__(self):
        return f"<CLIENTE: {self.nombre} - {self.telefono}>"
    
    
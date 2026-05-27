from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='templates')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///techbol.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)

    from app.blueprints.core.routes import bp_core
    from app.blueprints.clientes.routes import bp_cliente
    from app.blueprints.productos.routes import bp_productos
    from app.blueprints.pedidos.routes import bp_pedidos

    app.register_blueprint(bp_core)
    app.register_blueprint(bp_cliente, url_prefix="/clientes")
    app.register_blueprint(bp_productos, url_prefix="/productos")
    app.register_blueprint(bp_pedidos, url_prefix="/pedidos")  
    
    return app
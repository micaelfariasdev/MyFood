from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

pedido_produto = db.Table('pedido_produto',
    db.Column('pedido_id', db.Integer, db.ForeignKey('pedido.id'), primary_key=True),
    db.Column('produto_id', db.Integer, db.ForeignKey('produtos.id'), primary_key=True)
)

@login_manager.user_loader
def load_user(user_id):
    return Empresa.query.get(user_id)

class Empresa(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.now())
    user = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)
    nome = db.Column(db.String, nullable=False)
    razao_social = db.Column(db.String, nullable=False)
    cnpj = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    telefone = db.Column(db.String, nullable=False)
    endereco = db.Column(db.JSON, nullable=False)  # Usando JSON para armazenar o endereço como lista
    produtos = db.relationship('Produtos', backref='empresa', lazy=True)
    pedidos = db.relationship('Pedido', backref='empresa', lazy=True)
    clientes = db.relationship('Cliente', backref='empresa', lazy=True)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.now())
    nome = db.Column(db.String, nullable=False)
    telefone = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    endereco = db.Column(db.JSON, nullable=False)  # Usando JSON para armazenar o endereço como lista
    pedidos_historico = db.relationship('Pedido', backref='cliente', lazy=True)  # Relacionamento com a tabela Pedidos
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)

    def __repr__(self):
        return f'<Cliente {self.nome}>'
    
class Produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    descrição = db.Column(db.String, nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    quantidade = db.Column(db.Integer, nullable=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String, nullable=False, unique=True)  # Código único do pedido
    data = db.Column(db.DateTime, default=datetime.now())
    descricao = db.Column(db.String, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    produtos = db.relationship('Produtos', secondary=pedido_produto, backref='pedidos', lazy=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)

    def __repr__(self):
        return f'<Pedido {self.codigo}>'
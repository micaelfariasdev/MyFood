from app import db
from flask import flash
from app.models import *

def addproduto(cliente_id, produto_id, quantidade=1):
    carrinho = Carrinho.query.filter_by(cliente_id=cliente_id).first()

    item = CarrinhoProduto.query.filter_by(carrinho_id=carrinho.id, produto_id=produto_id).first()

    if item:
        item.quantidade += quantidade  # Atualiza a quantidade do produto no carrinho
    else:
        item = CarrinhoProduto(carrinho_id=carrinho.id, produto_id=produto_id, quantidade=quantidade)
        db.session.add(item)

    db.session.commit()

    return flash('Item cadastrada com sucesso!', 'success')
        

def gerar_codigo_unico():
    # Gerar o código aleatório
    import random
    import string
    codigo_aleatorio = '#' + ''.join(random.choices(string.ascii_letters + string.digits, k=5)).upper()

    # Verificar se o código já existe
    codigos_cadastrados = Pedido.query.filter_by(codigo=codigo_aleatorio).first()

    # Se o código já estiver cadastrado, gerar um novo código
    while codigos_cadastrados:
        codigo_aleatorio = '#' + ''.join(random.choices(string.ascii_letters + string.digits, k=5)).upper()
        codigos_cadastrados = Pedido.query.filter_by(codigo=codigo_aleatorio).first()

    return codigo_aleatorio

class produto_dic():
    def __init__(self, nome, valor, quantidade):
        self.nome = nome
        self.valor = valor
        self.quantidade = quantidade
        self.valort = quantidade * valor

    def __call__(self):
        return {
    'nome':self.nome,
    'valor':self.valor,
    'quantidade':self.quantidade,
    'valort':self.valort
}
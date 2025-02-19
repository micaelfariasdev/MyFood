from app import app, db
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import *
from app.forms import *
from app.services import *
from sqlalchemy import desc
from werkzeug.security import check_password_hash

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()  # Instanciando o formulário de login
    if form.validate_on_submit():  # Verifica se o formulário foi submetido e é válido
        # Obtém o usuário com base no e-mail
        user = Empresa.query.filter_by(user=form.user.data).first()

        # Verifica se o usuário existe e se a senha está correta
        if user and check_password_hash(user.senha, form.senha.data):
            login_user(user)  # Realiza o login do usuário
            return redirect(url_for('index'))  # Redireciona para a página desejada após o login
        else:
            flash('Credenciais inválidas. Tente novamente.', 'danger')  # Exibe uma mensagem de erro se não for encontrado ou a senha estiver incorreta

    return render_template('index.html', form=form, current_user=current_user)  # Renderiza o template de login

@app.route('/#logout')
@login_required  
def logout():
    logout_user()  # Faz o logout do usuário
    return redirect(url_for('index'))

@app.route('/cadastrar/', methods=['GET', 'POST'])
def cadastrar_empresa():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = EmpresaForm()
    

    if form.validate_on_submit():
        # Chama o método save() do formulário para salvar a empresa
        form.save()

        return redirect(url_for('index'))  # Redireciona para o dashboard da empresa
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Erro no campo {getattr(form, field).label.text}: {error}', 'danger')
    return render_template('cadastrar_empresa.html', form=form)

@app.route('/clientes/')
@login_required
def clientes():
    clientes = Cliente.query.filter_by(empresa_id=current_user.id).all()
    return render_template('clientes.html', clientes=clientes)

@app.route('/clientes/novo/', methods=['get', 'post'])
@login_required
def cadastro_cliente():
    login_user= current_user.id
    form = ClienteForm()
    if form.validate_on_submit():
        form.save(empresa_id=login_user)
        return redirect(url_for('index'))

    return render_template('cadastro_cliente.html', form=form)


@app.route('/produtos/novo/', methods=['GET', 'POST'])
@login_required
def novo_produto():
    form = ProdutosForm(empresa_id=current_user.id)

    
    if form.validate_on_submit():
        form.save(empresa_id=current_user.id)
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Erro no campo {getattr(form, field).label.text}: {error}', 'danger')
    return render_template('novo_produto.html', form=form)

@app.route('/produtos/')
@login_required
def produtos():
    produtos = Produtos.query.filter_by(empresa_id=current_user.id).all()
    return render_template('produtos.html', produtos=produtos)  

@app.route('/pedidos/')
@login_required
def pedidos():
    pedidos = Pedido.query.filter_by(empresa_id=current_user.id).order_by(desc(Pedido.data)).all()
    return render_template('pedidos.html', pedidos=pedidos)  


@app.route('/clientes/<int:id>/carinho', methods=['get', 'post'])
@login_required
def carrinho(id):
    carrinho = Carrinho.query.filter_by(cliente_id=id).fist()
    cliente = Cliente.query.filter_by(cliente_id=id).fist()

    if not carrinho:
        carrinho = Carrinho(cliente_id=id)
        db.session.add(carrinho)
        db.session.commit()
    return render_template('carrinho', carrinho=carrinho, cliente=cliente)

@app.route('/clientes/<int:id>/vendas/', methods=['GET', 'POST'])
@login_required
def vendas(id):
    produtos = Produtos.query.filter_by(empresa_id=current_user.id).all()
    return render_template('produtos.html', produtos=produtos, id=id)

@app.route('/clientes/<int:id>/vendas/<int:produto_id>/', methods=['POST','Get'])
@login_required
def addcarinho(id, produto_id):
    # Pegando o ID do cliente logado
    cliente_id = id

    # Verificar se já existe um carrinho para esse cliente
    carrinho = Carrinho.query.filter_by(cliente_id=cliente_id).first()
    if not carrinho:
        # Se não existir, cria um novo carrinho
        carrinho = Carrinho(cliente_id=cliente_id)
        db.session.add(carrinho)
        db.session.commit()

    # Verifica se o produto já está no carrinho
    item = CarrinhoProduto.query.filter_by(carrinho_id=carrinho.id, produto_id=produto_id).first()

    if item:
        # Se o produto já estiver no carrinho, aumenta a quantidade
        item.quantidade += 1
    else:
        # Se não, cria um novo item no carrinho
        item = CarrinhoProduto(carrinho_id=carrinho.id, produto_id=produto_id, quantidade=1)
        db.session.add(item)

    db.session.commit()

    flash('Produto adicionado ao carrinho com sucesso!', 'success')
    return redirect(url_for('vendas', id=id))  # Redireciona de volta para a página de produtos


@app.route('/clientes/<int:id>/cart/', methods=['GET', 'POST'])
@login_required
def cart(id):
    
    cliente = Cliente.query.get(id)
    carrinho = Carrinho.query.filter_by(cliente_id=cliente.id).first()
    
    if not carrinho:
        cart = Carrinho(
            cliente_id=id,

        )   

        db.session.add(cart)
        db.session.commit
        flash('Carrinho criado com sucesso.', 'success')
        return redirect(url_for('vendas', id=id))
    
    # Buscar produtos no carrinho
    produtos_no_carrinho = db.session.query(CarrinhoProduto, Produtos).join(Produtos).filter(CarrinhoProduto.carrinho_id == carrinho.id).all()

    carrinhodic = []
    total = 0
    for carrinho_produto, produto in produtos_no_carrinho:
        valor = carrinho_produto.quantidade * produto.valor
        total += valor
        estoque=Produtos.query.get(produto.id)
        
        item = {
            'nome': produto.nome,
            'valor': float(produto.valor),
            'quantidade': carrinho_produto.quantidade,
            'valort': float(valor)
        }
        carrinhodic.append(item)

    carrinhodic_json = dumps(carrinhodic)  # Converte a lista para JSON

    form = PedidoForm(
        codigo=gerar_codigo_unico(),
        valor=total,
        produtos=carrinhodic_json,  # Agora `produtos` está em JSON corretamente
        cliente_id=id
    )

    if form.validate_on_submit():
        form.save()  # Agora o método `save()` do formulário será chamado corretamente
        db.session.delete(carrinho)  # Remove o pedido
        db.session.commit()
        if estoque:
            if estoque.quantidade:
                print(carrinho_produto.quantidade)
                estoque.quantidade -= carrinho_produto.quantidade  # Novo valor
                print(estoque.quantidade)
                db.session.commit()
        return redirect(url_for('pedidos'))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Erro no campo {getattr(form, field).label.text}: {error}', 'danger')

    return render_template('carrinho.html', produtos=produtos_no_carrinho, id=id, cliente=cliente, total=total, form=form, )

@app.route('/clientes/<int:id>/cart/decrease/<int:produto_id>', methods=['GET'])
@login_required
def diminuir_quantidade(id, produto_id):
    # Buscar o carrinho do cliente
    carrinho = Carrinho.query.filter_by(cliente_id=id).first()

    if not carrinho:
        flash('Carrinho não encontrado.', 'error')
        return redirect(url_for('cart', id=id))

    # Buscar o item no carrinho pelo ID do produto
    item_carrinho = CarrinhoProduto.query.filter_by(carrinho_id=carrinho.id, produto_id=produto_id).first()

    if item_carrinho:
        # Se a quantidade for maior que 1, diminui 1
        if item_carrinho.quantidade > 1:
            item_carrinho.quantidade -= 1
            db.session.commit()  # Salva a alteração no banco
            flash('Quantidade do produto diminuída!', 'success')
        # Se a quantidade for igual a 1, remove o item do carrinho
        elif item_carrinho.quantidade == 1:
            db.session.delete(item_carrinho)  # Remove o item
            db.session.commit()  # Salva a alteração no banco
            flash('Produto removido do carrinho!', 'success')
    else:
        flash('Produto não encontrado no carrinho.', 'error')

    return redirect(url_for('cart', id=id))  # Redireciona para a página do carrinho


@app.route('/clientes/<int:id>/cart/increase/<int:produto_id>', methods=['get'])
@login_required
def aumentar_quantidade(id, produto_id):
    # Buscar o carrinho do cliente
    carrinho = Carrinho.query.filter_by(cliente_id=id).first()

    if not carrinho:
        flash('Carrinho não encontrado.', 'error')
        return redirect(url_for('cart', id=id))

    # Buscar o item do produto no carrinho
    item_carrinho = CarrinhoProduto.query.filter_by(carrinho_id=carrinho.id, produto_id=produto_id).first()

    if item_carrinho:
        item_carrinho.quantidade += 1  # Aumenta a quantidade em 1
        db.session.commit()  # Salva a alteração no banco
        flash('Quantidade do produto aumentada!', 'success')
    else:
        flash('Produto não encontrado no carrinho.', 'error')

    return redirect(url_for('cart', id=id))  # Redireciona para a página do carrinho



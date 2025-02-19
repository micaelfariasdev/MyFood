from app import app, db
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import *
from app.forms import *
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

@app.route('/pedidos/novo/', methods=['GET', 'POST'])
@login_required
def cadastrar_pedido():
    codigo_gerado = gerar_codigo_unico()
    form = PedidoForm(empresa_id=current_user.id, codigo=codigo_gerado)  # Passando o ID da empresa logada para o formulário
    if form.validate_on_submit():
        # Usando a função save para salvar o pedido
        form.save(empresa_id=current_user.id, codigo=codigo_gerado)

        flash('Pedido cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_pedidos'))

    return render_template('novo_pedido.html', form=form)

@app.route('/produtos/novo/', methods=['GET', 'POST'])
@login_required
def novo_produto():
    form = ProdutosForm()
    
from app import db
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from app.models import *
from flask_login import login_user, current_user
from flask import flash
from json import dumps
from werkzeug.security import generate_password_hash


estados = [
    ('', ''),
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins')
]


class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = EmailField('E-Mail', validators=[DataRequired()])
    telefone = TelField('Telefone', validators=[DataRequired(), Length(4, 16)])
    end_rua = StringField('Endereço', validators=[DataRequired()])
    end_numero = StringField('Número', validators=[DataRequired()])
    end_bairro = StringField('Bairrro', validators=[DataRequired()])
    end_cidade = StringField('Cidade', validators=[DataRequired()])
    end_estado = SelectField('Estado', choices=estados,
                             validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

    def save(self, empresa_id):
        endereco = {
            'Rua': self.end_rua.data,
            'Numero': self.end_numero.data,
            'Bairro': self.end_bairro.data,
            'Cidade': self.end_cidade.data,
            'Estado': self.end_estado.data,
        }

        cliente = Cliente(
            nome=self.nome.data,
            telefone=self.telefone.data,
            email=self.email.data,
            endereco=dumps(endereco),
            empresa_id=empresa_id
        )

        db.session.add(cliente)
        db.session.commit()

        flash('Cliente cadastrada com sucesso!', 'success')


class ProdutoForm(FlaskForm):
    nome = StringField('')
    valor = FloatField('')
    quantidade = IntegerField('')
    valort = FloatField('')


class PedidoForm(FlaskForm):
    codigo = StringField('Código')
    descricao = StringField('Descrição')
    valor = FloatField('Valor do Pedido')
    quantidade = IntegerField('Valor do Pedido')
    cliente_id = IntegerField('Cliente', validators=[DataRequired()])
    produtos = TextAreaField('Produtos', validators=[DataRequired()])
    submit = SubmitField('Cadastrar Pedido')

    def save(self):
        from json import loads  # Importar para converter JSON de string para lista de dicionários
        from app import db, Pedido  # Evitar erro de importação circular

        # Converter produtos de JSON (string) para lista de dicionários
        produtos_json = loads(self.produtos.data)

        # Criar o novo pedido
        novo_pedido = Pedido(
            codigo=self.codigo.data,
            descricao=self.descricao.data,
            valor=self.valor.data,
            produtos=produtos_json,  # Agora está correto para db.JSON
            cliente_id=self.cliente_id.data,
            empresa_id=current_user.id
        )

        # Salvar no banco
        db.session.add(novo_pedido)
        db.session.commit()

        flash('Pedido feito com sucesso!', 'success')
        return novo_pedido


class EmpresaForm(FlaskForm):
    # Campos do formulário da empresa
    user = StringField('Usuário', validators=[
                       DataRequired(), Length(min=4, max=50)])
    senha = PasswordField('Senha', validators=[
                          DataRequired(), Length(min=6, max=20)])
    confirmsenha = PasswordField('Confirme sua senha', validators=[
                                 DataRequired(), EqualTo('senha'), Length(min=6, max=20)])
    nome = StringField('Nome da Empresa', validators=[DataRequired()])
    razao_social = StringField('Razão Social', validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[DataRequired(), Length(max=18)])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    end_rua = StringField('Endereço', validators=[DataRequired()])
    end_numero = StringField('Número', validators=[DataRequired()])
    end_bairro = StringField('Bairrro', validators=[DataRequired()])
    end_cidade = StringField('Cidade', validators=[DataRequired()])
    # Aqui você pode usar JSON ou string simples para o endereço
    end_estado = SelectField('Estado', choices=estados,
                             validators=[DataRequired()])

    submit = SubmitField('Cadastrar Empresa')

    def validate_user(self, field):
        user = Empresa.query.filter_by(user=field.data).first()
        if user:
            raise ValidationError(
                'O nome de usuário já está em uso. Escolha outro.')

    def save(self):
        endereco = {
            'Rua': self.end_rua.data,
            'Numero': self.end_numero.data,
            'Bairro': self.end_bairro.data,
            'Cidade': self.end_cidade.data,
            'Estado': self.end_estado.data,
        }
        senha_hash = generate_password_hash(self.senha.data)
        nova_empresa = Empresa(
            user=self.user.data,
            senha=senha_hash,  # Lembre-se de hash a senha antes de salvar!
            nome=self.nome.data,
            razao_social=self.razao_social.data,
            cnpj=self.cnpj.data,
            email=self.email.data,
            telefone=self.telefone.data,
            endereco=endereco,  # Passando o dicionário para o campo 'endereco'
        )

        # Adiciona a empresa ao banco de dados
        db.session.add(nova_empresa)
        db.session.commit()

        # Realiza login automaticamente após o cadastro
        login_user(nova_empresa)

        flash('Empresa cadastrada com sucesso!', 'success')


class LoginForm(FlaskForm):
    user = StringField('Usuario', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')


class ProdutosForm(FlaskForm):
    nome = StringField('Nome do Produto', validators=[DataRequired()])
    descricao = StringField('Descrição', validators=[DataRequired()])
    valor = FloatField('Valor', validators=[DataRequired()])
    estoque = BooleanField('Tem estoque?', validators=[Optional()])
    quantidade = IntegerField('Quantidade em estoque', validators=[Optional()])
    submit = SubmitField('Cadastrar')

    def save(self, empresa_id):
        produto = Produtos(
            nome=self.nome.data,
            descricao=self.descricao.data,
            valor=self.valor.data,
            quantidade=self.quantidade.data,
            empresa_id=empresa_id
        )

        db.session.add(produto)
        db.session.commit()

        flash('Produto cadastrada com sucesso!', 'success')

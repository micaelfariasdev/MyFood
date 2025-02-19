from app import db
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from app.models import *
from flask_login import login_user
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
    nome = StringField('Nome' , validators=[DataRequired()])
    email = EmailField('E-Mail', validators=[DataRequired()])
    telefone = TelField('Telefone', validators=[DataRequired(), Length(4, 16)])
    end_rua = StringField('Endereço', validators=[DataRequired()])
    end_numero = StringField('Número', validators=[DataRequired()])
    end_bairro = StringField('Bairrro', validators=[DataRequired()])
    end_cidade = StringField('Cidade', validators=[DataRequired()])
    end_estado = SelectField('Estado', choices=estados, validators=[DataRequired()])
    submit = SubmitField('Cadastrar')
    

    

    def save(self, empresa_id):
        endereco={
        'Rua' : self.end_rua.data,
        'Numero' : self.end_numero.data,
        'Bairro' : self.end_bairro.data,
        'Cidade' : self.end_cidade.data,
        'Estado': self.end_estado.data,
    }
        cliente = Cliente(
            nome = self.nome.data,
            telefone = self.telefone.data,
            email = self.email.data,
            endereco = dumps(endereco),
            empresa_id = empresa_id
        )
        db.session.add(cliente)
        db.session.commit()
   

class PedidoForm(FlaskForm):
    def __init__(self, empresa_id, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)

        # Busca clientes dessa empresa
        self.cliente_id.choices = [
            (c.id, c.nome) for c in Cliente.query.filter_by(empresa_id=empresa_id).all()
        ]

        # Busca produtos dessa empresa
        self.produtos.choices = [
            (p.id, p.nome) for p in Produtos.query.filter_by(empresa_id=empresa_id).all()
        ]

    
    codigo = StringField('Código', validators=[DataRequired()], render_kw={"readonly": True})
    descricao = TextAreaField('Descrição')
    valor = FloatField('Valor do Pedido')
    cliente_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    produtos = SelectMultipleField('Produtos', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Cadastrar Pedido')

    def save(self, empresa_id, codigo):
        
        # Criar o novo pedido com os dados do formulário
        novo_pedido = Pedido(
            codigo=codigo,
            descricao=self.descricao.data,
            valor=self.valor.data,
            cliente_id=self.cliente_id.data,
            empresa_id=empresa_id
        )

        # Relacionando os produtos ao pedido
        for produto_id in self.produtos.data:
            produto = Produtos.query.get(produto_id)
            novo_pedido.produtos.append(produto)

        # Salvar o pedido no banco de dados
        db.session.add(novo_pedido)
        db.session.commit()
        return novo_pedido

class EmpresaForm(FlaskForm):
    # Campos do formulário da empresa
    user = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=50)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=20)])
    confirmsenha = PasswordField('Confirme sua senha', validators=[DataRequired(), EqualTo('senha'),Length(min=6, max=20)])
    nome = StringField('Nome da Empresa', validators=[DataRequired()])
    razao_social = StringField('Razão Social', validators=[DataRequired()])
    cnpj = IntegerField('CNPJ', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    end_rua = StringField('Endereço', validators=[DataRequired()])
    end_numero = StringField('Número', validators=[DataRequired()])
    end_bairro = StringField('Bairrro', validators=[DataRequired()])
    end_cidade = StringField('Cidade', validators=[DataRequired()])
    end_estado = SelectField('Estado', choices=estados, validators=[DataRequired()])  # Aqui você pode usar JSON ou string simples para o endereço
    
    submit = SubmitField('Cadastrar Empresa')

    def validate_user(self, field):
        user = Empresa.query.filter_by(user=field.data).first()
        if user:
            raise ValidationError('O nome de usuário já está em uso. Escolha outro.')

    def save(self):
        endereco={
        'Rua' : self.end_rua.data,
        'Numero' : self.end_numero.data,
        'Bairro' : self.end_bairro.data,
        'Cidade' : self.end_cidade.data,
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
    nome =StringField('Nome do Produto', validators=[DataRequired()])
    descricao=StringField('Descrição', validators=[DataRequired()])
    valor=FloatField('Valor', validators=[DataRequired()])
    estoque =BooleanField('Tem estoque?', validators=[Optional()])
    quantidade=IntegerField('Quantidade em estoque')

    def save(self, empresa_id):
        produto = ProdutosForm(
            nome=self.nome.data,
            descricao=self.descricao.data,
            valor=self.valor.data,
            quantidade=self.quantidade.data,
            empresa_id=empresa_id
        )

        db.session.add(produto)
        db.session.commit()

        # Realiza login automaticamente após o cadastro

        flash('Produto cadastrada com sucesso!', 'success')
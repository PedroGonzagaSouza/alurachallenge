
from enum import unique
from flask import Flask, jsonify, request, make_response # Para fazer o sistema web
from flask_sqlalchemy import SQLAlchemy #Para acessar o banco de dados
from marshmallow_sqlalchemy import SQLAlchemySchema #Serializar o banco
from marshmallow import fields

# Instanciando o Flask
app = Flask(__name__) 

#Configurando caminho para banco de dados
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:201019@localhost:3306/alurachallenge'

# Instanciando o SQLAlchemy como db, nas configs do app Flask
db = SQLAlchemy(app)

#Criando banco de dados como classe
class Videos(db.Model):
    __tablename__ = "Vídeos"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.String(200))
    url = db.Column(db.String(200), unique=True)

    #Função para criar banco de dados dentro do app
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    #Método construtor da classe para o banco de dados
    def __init__(self, titulo, descricao, url):
        self.titulo = titulo
        self.descricao = descricao
        self.url = url

    #Método para representar através de string
    def __repr__(self):
        return '' %self.id

db.create_all()
    


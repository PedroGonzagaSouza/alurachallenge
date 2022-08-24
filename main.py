
from enum import unique
import json
from operator import methodcaller
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
    
#Mapear as variáveis para os atributos da classe Videos

class VideosSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta): #Definir model para relacionar com o schema, para retornar JSON
        model = Videos
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    titulo = fields.String(required=True)
    descricao = fields.String(required=True)
    url = fields.String(required=True)

'''Rotas e métodos Flask'''

#Fazendo página index para retornar todos os vídeos
@app.route('/videos', methods=['GET'])
def index():
    getVideos = Videos.query.all() #Buscando todos os itens da tabela Vídeos
    videosSchema = VideosSchema(many=True) #Instanciando videosSchema como objeto da classe VideosSchema
    videos = videosSchema.dump(getVideos) 
    return make_response(jsonify({"Vídeos":videos}))

#Método GET para cada vídeo por id
@app.route('/videos/<id>', methods=['GET'])
def getVideoById(id):
    getVideo = Videos.query.get(id)
    videosSchema = VideosSchema()
    video = videosSchema.dump(getVideo)
    return make_response(jsonify({"Vídeo": video}))


#Fazendo método post para adicionar á página videos
@app.route('/videos', methods=['POST'])
def createVideo():
    data = request.get_json() #Pegando formato JSON
    videosSchema = VideosSchema() #Instanciando novo objeto na classe VideosSchema
    videos = videosSchema.load(data) #Carregando dados na variável videos
    result = videosSchema.dump(videos.create()) #Criando retorno na variável result
    return make_response(jsonify({"Vídeos":result}), 200) #Retornando a variável result como JSON


#Fazendo método PUT para atualizar a página videos
@app.route('/videos/<id>', methods=['PUT'])
def atualizarVideoById(id):
    data = request.get_json()
    getVideos = Videos.query.get(id)
    if data.get('titulo'):
        getVideos.titulo = data['titulo']
    if data.get('descricao'):
        getVideos.descricao = data['descricao']
    if data.get('url'):
        getVideos.url = data['url']
    
    db.session.add(getVideos)
    db.session.commit()
    VideosSchema = VideosSchema(only=['id', 'titulo', 'descricao', 'url'])
    videos = videosSchema.dump(getVideos)
    return make_response(jsonify({'Vídeos': videos}))


#Método DELETE
@app.route('/videos/<id>', methods=['DELETE'])
def deleteVideoById(id):
    getVideos = db.query.get(id)
    db.session.delete(getVideos)
    db.session.commit()
    return make_response('', 204)


if __name__=="__main__":
    app.run(debug=True)

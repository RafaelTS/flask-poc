from flask import Flask, request
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel
from tinydb import TinyDB

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Poc Python-Flask')
spec.register(server)
database = TinyDB('database.json')

class Pessoa(BaseModel) :
    id: int
    nome: str
    idade: int

@server.get('/pessoas')
def pegar_pessoas():
    """Busca pessoas no banco de dados"""
    return 'Vamos buscar os doletas'

@server.post('/pessoas')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_200=Pessoa))

def inserir_pessoa():
    """Insere uma pessoa no banco de dados"""
    body = request.context.body.dict()
    database.insert(body)
    return body
    

server.run()
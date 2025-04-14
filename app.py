from itertools import count
from typing import Optional
from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel, Field
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Poc Python-Flask')
spec.register(server)
database = TinyDB(storage=MemoryStorage)
c = count()

class People(BaseModel) :
    id: Optional[int] = Field(default_factory=lambda: next(c))
    name: str
    age: int

class Peoples(BaseModel) :
    peoples: list[People]
    count: int

@server.get('/peoples')
@spec.validate(resp=Response(HTTP_200=Peoples))
def get_peoples():
    """Return all people from my database"""
    return jsonify(
        Peoples(
            peoples=database.all(),
            count=len(database.all())
        ).dict()
    )

@server.get('/peoples/<int:id>')
@spec.validate(resp=Response(HTTP_200=People))
def get_people(id):
    """Return all people from my database"""
    try:
        pessoa = database.search(Query().id == id)[0]
    except IndexError:
        return {'message': 'People not found!'}, 404
    return jsonify(pessoa)


@server.post('/peoples')
@spec.validate(body=Request(People), resp=Response(HTTP_200=People))

def insert_peoples():
    """Insert a people in the database"""
    body = request.context.body.dict()
    database.insert(body)
    return body    

@server.put('/peoples/<int:id>')
@spec.validate(
    body=Request(People), resp=Response(HTTP_200=People)
)
def update_people(id):
    """Update a people from my database"""
    People = Query()
    body = request.context.body.dict()
    database.update(body, People.id == id)
    return jsonify(body)

@server.delete('/peoples/<int:id>')
@spec.validate(resp=Response('HTTP_204'))

def delete_people(id):
    """Delete a people from my database"""
    People = Query()
    database.remove(People.id == id)
    return jsonify({})


server.run()
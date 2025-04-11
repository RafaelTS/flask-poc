from typing import Optional
from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel
from tinydb import TinyDB, Query

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Poc Python-Flask')
spec.register(server)
database = TinyDB('database.json')

class People(BaseModel) :
    id: Optional[int]
    name: str
    age: int

class Peoples(BaseModel) :
    peoples: list[People]
    count: int

@server.get('/peoples')
@spec.validate(resp=Response(HTTP_200=Peoples))
def get_people():
    """Return all people from my database"""
    return jsonify(
        Peoples(
            peoples=database.all(),
            count=len(database.all())
        )
    )

@server.post('/people')
@spec.validate(body=Request(Peoples), resp=Response(HTTP_200=Peoples))

def insert_people():
    """Insert a people in the database"""
    body = request.context.body.dict()
    database.insert(body)
    return body    


server.run()
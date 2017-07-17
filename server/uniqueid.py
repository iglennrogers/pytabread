from sqlalchemy import Column, String
import uuid


def defn():
    return Column(String(50))


def newvalue():
    return str(uuid.uuid4())

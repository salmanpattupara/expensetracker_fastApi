from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 

from api.main import app


Client = TestClient(app)

def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    print("Setup for test_main module")
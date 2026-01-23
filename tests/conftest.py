import pytest
from contextlib import contextmanager
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from curso_fastapi.app import app
from curso_fastapi.models import table_registry

from sqlalchemy import create_engine, event


@pytest.fixture
def client():
    return TestClient(app=app)


@pytest.fixture
def session():
    # engine :
    # cria um mecanismo de bd SQLite em memória usando SQLAlchemy

    # table_registry.metadata.create_all(engine) :
    # cria todas as tabelas no bd de teste antes de
    # cada teste que usa a fixture session

    # yield session :
    # fornece uma instância de Session que será injetada
    # em cada teste que solicita a fixture session

    # table_registry.metadata.drop_all(engine) :
    # após cada teste que usa a fixture session
    # elimina -> todas as tabelas do bd de teste
    # garante -> que cada teste seja executado contra um bd limpo

    # engine.dispose :
    # fecha todas as conexões abertas associadas ao engine
    # libera os recursos do sistema
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()

# o decorator contextmanager : 
# Cria um gerenciador de contexto para que a
# função _mock_db_time seja usada com um bloco with.
@contextmanager
def _mock_db_time(*, model, time=datetime(2026,1,1)):

    # definição do hook
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
    
    # add um evento a um model que será passado a função
    # o hook será executado 'antes da inserção' do evento
    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    # remoção do hook após o final do gerenciamento de contexto
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time
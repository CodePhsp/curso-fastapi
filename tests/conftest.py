from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from curso_fastapi.app import app
from curso_fastapi.database import get_session
from curso_fastapi.models import User, table_registry
from curso_fastapi.security import Settings, get_password_hash


@pytest.fixture
def settings():
    return Settings()


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )

    return response.json()['access_token']


@pytest.fixture
def user(session):
    password = 'mypass'
    user = User(
        username='Teste',
        email='teste@test.com',
        password=get_password_hash('mypass'),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password  # pyright: ignore[reportAttributeAccessIssue]

    return user


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        # Substitui a função get_session que usamos para a aplicação
        # real, pela nossa função que retorna a fixture de testes.
        app.dependency_overrides[get_session] = get_session_override
        yield client

    # Limpa a sobrescrita que fizemos no app para usar a fixture de session.
    app.dependency_overrides.clear()


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
    engine = create_engine(
        'sqlite:///:memory:',
        # permite que a conexão seja compartilhada entre
        # threads diferentes sem levar a erros.
        connect_args={'check_same_thread': False},
        # garante que as duas threads usem o mesmo canal de comunicação,
        # evitando erros relacionados ao uso de diferentes
        # conexões em threads diferentes.
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()


# o decorator contextmanager :
# Cria um gerenciador de contexto para que a
# função _mock_db_time seja usada com um bloco with.
@contextmanager
def _mock_db_time(*, model, time=datetime(2026, 1, 1)):

    # definição do hook
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    # add um evento a um model que será passado a função
    # o hook será executado 'antes da inserção' do evento
    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    # remoção do hook após o final do gerenciamento de contexto
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time

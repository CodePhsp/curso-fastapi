from http import HTTPStatus

from fastapi.testclient import TestClient

from curso_fastapi.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)

    response = client('/')
    assert response.status_code == HTTPStatus.OK


def test_root_retorna_hello_em_html():
    client = TestClient(app)

    response = client('hello')
    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo </h1>' in response.text

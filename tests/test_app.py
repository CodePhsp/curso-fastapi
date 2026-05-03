from http import HTTPStatus


def test_root_deve_retornar_200(client):

    response = client.get('/')

    assert response.json() == {'message': 'Curso fastAPI'}
    assert response.status_code == HTTPStatus.OK

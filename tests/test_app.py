from http import HTTPStatus

from curso_fastapi.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):

    response = client.get('/')
    assert response.status_code == HTTPStatus.OK


def test_root_deve_criar_usuario(client):

    response = client.post(
        '/users/',
        json={
            'username': 'Pedro',
            'email': 'pedro@gmail.com',
            'password': '123456',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Pedro',
        'email': 'pedro@gmail.com',
        'id': 1,
    }


def test_root_deve_retornar_todos_usuarios(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_busca_usuarios_com_usuarios(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.json() == {'users': [user_schema]}


def test_root_deve_atualizar_usuario(client, user):

    response = client.put(
        '/users/1',
        json={
            'username': 'Pedro',
            'email': 'pedro@gmail.com',
            'password': '123456',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Pedro',
        'email': 'pedro@gmail.com',
        'id': 1,
    }


def test_root_erro_de_integridade_ao_atualizar_usuario(client, user):

    client.post(
        '/users',
        json={
            'username': 'Pedro',
            'email': 'pedro@gmail.com',
            'password': '123456',
        },
    )

    response_update = client.put(
        f'/users/{user.id}',
        json={
            'username': 'Pedro',
            'email': 'pedro.henrique@test.com',
            'password': 'secretpass',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or email already exists.'
    }


def test_root_deve_excluir_usuario(client, user):

    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


# ATIVIDADE_03 - CAMINHO DO ERRO (raise HTTPException)
#                NOVO ENDPOIT PARA BUSCAR UM ÚNICO REGISTRO
def test_root_atualizar_usuario_caso_nao_encontrado(client):

    response = client.put(
        '/users/999',
        json={
            'username': 'bob',
            'email': 'bob@gmail.com',
            'password': 'oemail.@gmail.com',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


# NÃO FOI POSSÍVEL REALIZAR ESSE TESTE COM ÊXITO
def test_root_deve_buscar_um_unico_usuario(client):

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'username': 'Pedro',
        'email': 'pedro@gmail.com',
        'id': 1,
    }


def test_root_excluir_usuario_caso_nao_encontrado(client):

    response = client.delete('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_root_buscar_unico_usuario_caso_nao_encontrado(client):

    response = client.get('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
    
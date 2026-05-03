from http import HTTPStatus

from curso_fastapi.schemas import UserPublic


def test_deve_retornar_201_ao_criar_usuario(client):

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


def test_deve_retornar_200_ao_buscar_todos_usuarios_inexistentes(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_deve_retornar_200_ao_buscar_todos_usuarios_existentes(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.json() == {'users': [user_schema]}


def test_deve_retornar_200_ao_buscar_um_unico_usuario_existente(client, user):
    # Serelização dos dados para conformidade do schema definido
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get(f'/users/{user.id}')

    # Testa se status da resposta é 200 - OK
    assert response.status_code == HTTPStatus.OK

    # Testa se a resposta é igual o definido no schema
    assert response.json() == {'user': user_schema}


def test_deve_retornar_200_ao_atualizar_usuario_existente(client, user, token):

    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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
        'id': user.id,
    }


def test_deve_retornar_409_ao_atualizar_usuario_existente(client, user, token):

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
        headers={'Authorization': f'Bearer {token}'},
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


def test_deve_retornar_200_ao_excluir_usuario_existente(client, user, token):

    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}

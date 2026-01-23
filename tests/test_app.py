from http import HTTPStatus


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


# NÃO FOI POSSÍVEL REALIZAR ESSE TESTE COM ÊXITO
def test_root_deve_buscar_um_unico_usuario(client):

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'username': 'Pedro',
        'email': 'pedro@gmail.com',
        'id': 1,
    }


def test_root_deve_retornar_usuarios(client):

    response = client.get(
        '/users/',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'Pedro',
                'email': 'pedro@gmail.com',
                'id': 1,
            }
        ]
    }


def test_root_deve_atualizar_usuario(client):

    response = client.put(
        '/users/1',
        json={
            'username': 'Henrique',
            'email': 'henrique@gmail.com',
            'password': '2154896',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Henrique',
        'email': 'henrique@gmail.com',
        'id': 1,
    }


def test_root_deve_excluir_usuario(client):

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


def test_root_excluir_usuario_caso_nao_encontrado(client):

    response = client.delete('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}

def test_root_buscar_unico_usuario_caso_nao_encontrado(client):

    response = client.get('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}

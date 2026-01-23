from dataclasses import asdict

from sqlalchemy import select

from curso_fastapi.models import User


def test_create_user(session, mock_db_time):
    # .scalar :
    # método usado para performar buscas no banco (queries).

    with mock_db_time(model=User) as time:
        new_user = User(username='Pedro', password='123', email='test@gmail.com')
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'Pedro'))

    assert asdict(user) == {
        'id': 1,
        'username': 'Pedro',
        'password': 'secret',
        'email': 'teste@test',
        'created_at': time,
    }

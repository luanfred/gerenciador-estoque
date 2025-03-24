from http import HTTPStatus

import pytest
from pydantic import ValidationError

from app.schemas.users_schema import UsersSchemaCreate
from tests.utils import create_header_autorization

PREFIX = '/users'


def test_create_user(client):
    response = client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser', 'email': 'testuser@example.com', 'password': 'testpassword'},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'testuser'
    assert response.json()['email'] == 'testuser@example.com'


def test_create_user_existing_email(client):
    client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser2', 'email': 'testuser2@example.com', 'password': 'testpassword'},
    )
    response = client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser3', 'email': 'testuser2@example.com', 'password': 'testpassword'},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'User already registered with this email'


def test_create_user_existing_name(client):
    client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser4', 'email': 'testuser4@example.com', 'password': 'testpassword'},
    )
    response = client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser4', 'email': 'testuser5@example.com', 'password': 'testpassword'},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'User already registered with this name'


def test_login_user(client):
    email = 'testuser6@example.com'
    password = 'testpassword'
    client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser6', 'email': email, 'password': password},
    )
    response_login = client.post(
        f'{PREFIX}/login/',
        data={'username': email, 'password': password},
    )
    assert response_login.status_code == HTTPStatus.OK
    assert 'access_token' in response_login.json()
    assert 'token_type' in response_login.json()


def test_login_user_invalid_credentials(client):
    email = 'testuser6@example.com'
    password = 'testpassword'
    client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser6', 'email': email, 'password': password},
    )
    response_login = client.post(
        f'{PREFIX}/login/',
        data={'username': email, 'password': 'wrongpassword'},
    )
    assert response_login.status_code == HTTPStatus.UNAUTHORIZED


def test_get_user_by_id(client):
    email = 'testuser6@example.com'
    password = 'testpassword'
    response_user = client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser6', 'email': email, 'password': password},
    )
    headers = create_header_autorization(client, email, password)
    user_id = response_user.json()['id']
    response = client.get(f'{PREFIX}/{user_id}/', headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'testuser6'
    assert response.json()['email'] == 'testuser6@example.com'


def test_get_user_by_id_not_found(client):
    email = 'testuser6@example.com'
    password = 'testpassword'
    client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser6', 'email': email, 'password': password},
    )
    headers = create_header_autorization(client, email, password)
    response = client.get(f'{PREFIX}/999/', headers=headers)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_update_user(client):
    email = 'testuser7@example.com'
    password = 'testpassword'
    response = client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser7', 'email': email, 'password': password},
    )
    user_id = response.json()['id']
    headers = create_header_autorization(client, email, password)
    response = client.put(
        f'{PREFIX}/{user_id}/',
        json={'name': 'updateduser', 'email': 'updateduser@example.com', 'password': 'newpassword'},
        headers=headers,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'updateduser'
    assert response.json()['email'] == 'updateduser@example.com'


def test_update_user_not_found(client):
    email = 'testuser6@example.com'
    password = 'testpassword'
    client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser6', 'email': email, 'password': password},
    )
    headers = create_header_autorization(client, email, password)
    response = client.put(
        f'{PREFIX}/999/',
        json={'name': 'nonexistent', 'email': 'nonexistent@example.com', 'password': 'password'},
        headers=headers,
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_update_user_email_already_exists(client):
    # 1 - Create the first user
    nome = 'testuser1'
    email = 'testuser1@example.com'
    password = 'testpassword'
    response_user = client.post(
        f'{PREFIX}/register/',
        json={'name': nome, 'email': email, 'password': password},
    )
    user_id = response_user.json()['id']
    headers = create_header_autorization(client, email, password)

    # 2 - Create the second user
    nome_2 = 'testuser2'
    email_2 = 'testeemail2@example.com'
    client.post(
        f'{PREFIX}/register/',
        json={'name': nome_2, 'email': email_2, 'password': 'testpassword'},
    )

    # 3 - Attempt to update the first user with the second user's email
    response = client.put(
        f'{PREFIX}/{user_id}/',
        json={'name': 'testuser3', 'email': email_2, 'password': 'testpassword'},
        headers=headers,
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'User already registered with this email'

    # 4 - Attempt to update the second user with the first user's name
    response = client.put(
        f'{PREFIX}/{user_id}/',
        json={'name': nome_2, 'email': 'testeuser3@example.com', 'password': 'testpassword'},
        headers=headers,
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'User already registered with this name'


def test_delete_user(client):
    email = 'testuser8@example.com'
    password = 'testpassword'
    response = client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser8', 'email': email, 'password': password},
    )
    headers = create_header_autorization(client, email, password)
    user_id = response.json()['id']
    response = client.delete(f'{PREFIX}/{user_id}/', headers=headers)
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_not_found(client):
    email = 'testuser8@example.com'
    password = 'testpassword'
    response = client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser8', 'email': email, 'password': password},
    )
    headers = create_header_autorization(client, email, password)
    response = client.delete(f'{PREFIX}/999/', headers=headers)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_name_too_long():
    invalid_data = {
        'name': 'a' * 51,
        'email': 'john.doe@example.com',
        'password': 'securepassword123',
    }
    with pytest.raises(ValidationError) as exc_info:
        UsersSchemaCreate(
            email=invalid_data['email'],
            name=invalid_data['name'],
            password=invalid_data['password'],
        )
    assert 'Name must be less than 50 characters' in str(exc_info.value)


def test_email_too_long():
    invalid_data = {
        'name': 'John Doe',
        'email': 'a' * 51 + '@example.com',
        'password': 'securepassword123',
    }
    with pytest.raises(ValidationError) as exc_info:
        UsersSchemaCreate(
            email=invalid_data['email'],
            name=invalid_data['name'],
            password=invalid_data['password'],
        )
    assert 'Email must be less than 50 characters' in str(exc_info.value)


def test_password_too_long():
    invalid_data = {'name': 'John Doe', 'email': 'john.doe@example.com', 'password': 'a' * 51}
    with pytest.raises(ValidationError) as exc_info:
        UsersSchemaCreate(
            email=invalid_data['email'],
            name=invalid_data['name'],
            password=invalid_data['password'],
        )
    assert 'Password must be less than 50 characters' in str(exc_info.value)


def test_if_user_model_exists_in_file_all_models():
    from app.models.all_models import UsersModel  # noqa

    assert UsersModel is not None

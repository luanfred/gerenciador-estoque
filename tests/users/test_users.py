from http import HTTPStatus

import pytest
from pydantic import ValidationError

from app.schemas.users_schema import UsersSchemaCreate

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
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Email already registered'


def test_create_user_existing_name(client):
    client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser4', 'email': 'testuser4@example.com', 'password': 'testpassword'},
    )
    response = client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser4', 'email': 'testuser5@example.com', 'password': 'testpassword'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Name already registered'


def test_get_user_by_id(client):
    response = client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser6', 'email': 'testuser6@example.com', 'password': 'testpassword'},
    )
    user_id = response.json()['id']
    response = client.get(f'{PREFIX}/{user_id}/')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'testuser6'
    assert response.json()['email'] == 'testuser6@example.com'


def test_get_user_by_id_not_found(client):
    response = client.get(f'{PREFIX}/999/')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_get_all_users(client):
    list_users = [
        {'name': 'testuser7', 'email': 'testuser7@example.com', 'password': 'testpassword'},
        {'name': 'testuser8', 'email': 'testuser8@example.con', 'password': 'testpassword'},
    ]
    response = client.post(
        f'{PREFIX}/register/',
        json=list_users[0],
    )
    response = client.post(
        f'{PREFIX}/register/',
        json=list_users[1],
    )
    response = client.get(f'{PREFIX}/')
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == len(list_users)


def test_get_all_users_not_found(client):
    response = client.get(f'{PREFIX}/')
    print('response.json()', response.json())
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'No users found'


def test_update_user(client):
    response = client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser7', 'email': 'testuser7@example.com', 'password': 'testpassword'},
    )
    user_id = response.json()['id']
    response = client.put(
        f'{PREFIX}/{user_id}/',
        json={'name': 'updateduser', 'email': 'updateduser@example.com', 'password': 'newpassword'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'updateduser'
    assert response.json()['email'] == 'updateduser@example.com'


def test_update_user_not_found(client):
    response = client.put(
        f'{PREFIX}/999/',
        json={'name': 'nonexistent', 'email': 'nonexistent@example.com', 'password': 'password'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_delete_user(client):
    response = client.post(
        f'{PREFIX}/register/',
        json={'name': 'testuser8', 'email': 'testuser8@example.com', 'password': 'testpassword'},
    )
    user_id = response.json()['id']
    response = client.delete(f'{PREFIX}/{user_id}/')
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_not_found(client):
    response = client.delete(f'{PREFIX}/999/')
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
    from app.models.all_models import UsersModel # noqa
    assert UsersModel is not None

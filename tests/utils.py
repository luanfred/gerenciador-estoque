from fastapi.testclient import TestClient


def create_header_autorization(client: TestClient, email: str, password: str):
    response = client.post(
        url='users/login/',
        data={'username': email, 'password': password},
    )
    response_token = response.json()
    access_token = response_token['access_token']
    token_type = response_token['token_type']
    return {'Authorization': f'{token_type} {access_token}'}


def create_user_with_token(client: TestClient) -> dict:
    email = 'testuser6@example.com'
    password = 'testpassword'
    client.post(
        'users/register/',
        json={'name': 'testuser6', 'email': email, 'password': password},
    )
    response_token = client.post(
        url='users/login/',
        data={'username': email, 'password': password},
    )
    response_token = response_token.json()
    access_token = response_token['access_token']
    token_type = response_token['token_type']
    return {'Authorization': f'{token_type} {access_token}'}

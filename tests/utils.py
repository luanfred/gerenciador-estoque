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

from http import HTTPStatus

from tests.utils import create_user_with_token

PREFIX = '/products'

json = {
    'name': 'testproduct',
    'description': 'testdescription',
    'provider': 'testprovider',
    'brand': 'testbrand',
    'size': 'testsize',
    'photo_link': 'http://example.com/photo.jpg',
    'price': 10.99,
    'quantity': 100,
}


def test_create_product(client):
    response = client.post(
        f'{PREFIX}/',
        headers=create_user_with_token(client),
        json=json,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == json['name']
    assert response.json()['description'] == json['description']
    assert response.json()['provider'] == json['provider']
    assert response.json()['brand'] == json['brand']
    assert response.json()['size'] == json['size']
    assert response.json()['photo_link'] == json['photo_link']
    assert response.json()['price'] == json['price']
    assert response.json()['quantity'] == json['quantity']
    assert 'id' in response.json()


def test_get_all_products_no_products(client):
    response = client.get(
        f'{PREFIX}/',
        headers=create_user_with_token(client),
    )
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)


def test_get_all_products_with_products(client):
    client.post(
        f'{PREFIX}/',
        headers=create_user_with_token(client),
        json=json,
    )
    response = client.get(
        f'{PREFIX}/',
        headers=create_user_with_token(client),
    )
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_get_product_by_id(client):
    response = client.post(
        f'{PREFIX}/',
        headers=create_user_with_token(client),
        json=json,
    )
    product_id = response.json()['id']
    response = client.get(
        f'{PREFIX}/{product_id}',
        headers=create_user_with_token(client),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == product_id


def test_get_product_by_id_not_found(client):
    response = client.get(
        f'{PREFIX}/999',
        headers=create_user_with_token(client),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Product not found'


def test_update_product(client):
    response = client.post(
        f'{PREFIX}/',
        headers=create_user_with_token(client),
        json=json,
    )
    product_id = response.json()['id']
    updated_json = json.copy()

    updated_json['name'] = 'updatedproduct'
    updated_json['description'] = 'updateddescription'
    updated_json['provider'] = 'updatedprovider'
    updated_json['brand'] = 'updatedbrand'
    updated_json['size'] = 'updatedsize'
    updated_json['photo_link'] = 'http://example.com/updated_photo.jpg'
    updated_json['price'] = 20.99
    updated_json['quantity'] = 50

    response = client.put(
        f'{PREFIX}/{product_id}',
        headers=create_user_with_token(client),
        json=updated_json,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == updated_json['name']
    assert response.json()['description'] == updated_json['description']
    assert response.json()['provider'] == updated_json['provider']
    assert response.json()['brand'] == updated_json['brand']
    assert response.json()['size'] == updated_json['size']
    assert response.json()['photo_link'] == updated_json['photo_link']
    assert response.json()['price'] == updated_json['price']
    assert response.json()['quantity'] == updated_json['quantity']
    assert response.json()['id'] == product_id


def test_update_product_not_found(client):
    client.post(
        f'{PREFIX}/',
        headers=create_user_with_token(client),
        json=json,
    )

    updated_json = json.copy()
    updated_json['name'] = 'updatedproduct'

    response = client.put(
        f'{PREFIX}/999',
        headers=create_user_with_token(client),
        json=updated_json,
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_product(client):
    response = client.post(
        f'{PREFIX}/',
        headers=create_user_with_token(client),
        json=json,
    )
    product_id = response.json()['id']
    response = client.delete(
        f'{PREFIX}/{product_id}',
        headers=create_user_with_token(client),
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_product_not_found(client):
    client.post(
        f'{PREFIX}/',
        headers=create_user_with_token(client),
        json=json,
    )
    response = client.delete(
        f'{PREFIX}/999',
        headers=create_user_with_token(client),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Product not found'

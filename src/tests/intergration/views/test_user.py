from http_constants.headers import HttpHeaders


def test_login_user__return_200(client, login_body):
    response = client.post("api/user/login", json=login_body)
    assert response.status_code == 200
    assert "access_token" in response.json


def test_login_user__incorrect_password__return_400(client, login_body):
    login_body["password"] = "incorrect"
    response = client.post("api/user/login", json=login_body)
    assert response.status_code == 400
    assert response.json["message"] == "Invalid email or password"


def test_login_user__incorrect_email__return_400(client, login_body):
    login_body["email"] = "incorrect@google.com"
    response = client.post("api/user/login", json=login_body)
    assert response.status_code == 400
    assert response.json["message"] == "Invalid email or password"


def test_login_user__get_current_user_data__return_200(
    client, login_body, created_user
):
    response = client.post("api/user/login", json=login_body)

    assert response.status_code == 200
    access_token = response.json["access_token"]
    auth_header = {HttpHeaders.AUTHORIZATION: f"Bearer {access_token}"}

    response = client.get("api/user/current_user", json=login_body, headers=auth_header)
    assert response.status_code == 200
    assert response.json["email"] == created_user.email
    assert response.json["nickname"] == created_user.nickname
    assert response.json["user_id"] == created_user.user_id

def test_create_user__valid_body__return_201(client, valid_user_create_body):
    response = client.post("api/user", json=valid_user_create_body)
    assert response.status_code == 201

def test_create_user__same_email_nickname__return_400(client, valid_user_create_body):
    response = client.post("api/user", json=valid_user_create_body)
    assert response.status_code == 400

    response = client.post("api/user", json=valid_user_create_body)
    assert response.status_code == 400

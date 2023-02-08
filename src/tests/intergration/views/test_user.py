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

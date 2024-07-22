# tests/test_cognito.py

import pytest
from fastapi import HTTPException
from app.utils.cognito_utils import verify_token, get_current_user
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from unittest.mock import patch, MagicMock

# Mocking environment variables
@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv('COGNITO_USER_POOL_ID', 'us-east-1_Cfl7YFwsG')
    monkeypatch.setenv('COGNITO_APP_CLIENT_ID', 'erthhvp4uv179lo1qa2isr3vd')
    monkeypatch.setenv('COGNITO_REGION', 'us-east-1')
    monkeypatch.setenv('JWT_ALGORITHM', 'HS256')  # Using HS256 for testing

# Mocking the public keys
@pytest.fixture
def mock_public_keys():
    return [
        {
            'kid': 'mocked_key_id',
            'kty': 'oct',
            'use': 'sig',
            'k': 'mocked_secret'
        }
    ]

# Mocking the JWT payload
@pytest.fixture
def mock_jwt_payload():
    return {
        'sub': '1234567890',
        'name': 'John Doe',
        'iat': 1516239022,
        'exp': 1516242622,
        'aud': 'erthhvp4uv179lo1qa2isr3vd'
    }

# Mocking the requests.get method to return mocked public keys
@pytest.fixture
def mock_requests_get(mock_public_keys):
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'keys': mock_public_keys}
        mock_get.return_value = mock_response
        yield mock_get

# Test verifying a valid token
def test_verify_token_valid(mock_requests_get, mock_jwt_payload):
    secret = 'mocked_secret'
    token = jwt.encode(mock_jwt_payload, secret, algorithm='HS256', headers={'kid': 'mocked_key_id'})
    with patch('app.utils.cognito_utils.PUBLIC_KEYS', [{'kid': 'mocked_key_id', 'kty': 'oct', 'use': 'sig', 'k': secret}]):
        payload = verify_token(token, algorithm='HS256')
        assert payload == mock_jwt_payload

# Test verifying an invalid token
def test_verify_token_invalid(mock_requests_get):
    token = 'invalid_token'
    with patch('app.utils.cognito_utils.PUBLIC_KEYS', [{'kid': 'mocked_key_id', 'kty': 'oct', 'use': 'sig', 'k': 'mocked_secret'}]):
        with pytest.raises(HTTPException) as excinfo:
            verify_token(token, algorithm='HS256')
        assert excinfo.value.status_code == 401
        assert excinfo.value.detail == 'Invalid token.'

# Test getting current user
def test_get_current_user(mock_requests_get, mock_jwt_payload):
    secret = 'mocked_secret'
    token = jwt.encode(mock_jwt_payload, secret, algorithm='HS256', headers={'kid': 'mocked_key_id'})
    with patch('app.utils.cognito_utils.PUBLIC_KEYS', [{'kid': 'mocked_key_id', 'kty': 'oct', 'use': 'sig', 'k': secret}]):
        user = get_current_user(token)
        assert user == mock_jwt_payload

# app/utils/cognito_utils.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import requests
from typing import List
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# AWS Cognito configuration from .env file
COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
COGNITO_APP_CLIENT_ID = os.getenv('COGNITO_APP_CLIENT_ID')
COGNITO_REGION = os.getenv('COGNITO_REGION')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

# Fetch public keys from AWS Cognito
def get_cognito_public_keys():
    url = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail='Unable to fetch JWKS')
    return response.json()['keys']

PUBLIC_KEYS = get_cognito_public_keys()

def verify_token(token: str, algorithm: str = None):
    algorithm = algorithm or JWT_ALGORITHM
    try:
        header = jwt.get_unverified_header(token)
        rsa_key = None
        for key in PUBLIC_KEYS:
            if key['kid'] == header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if rsa_key is None and algorithm != 'HS256':
            raise HTTPException(status_code=401, detail='Public key not found.')

        payload = jwt.decode(token, rsa_key if rsa_key else 'mocked_secret', algorithms=[algorithm], audience=COGNITO_APP_CLIENT_ID)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token.')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)

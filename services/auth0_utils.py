import json
import requests
import jwt
from jwt import PyJWKClient
import os

import sys
sys.path.append('../')

auth0_app_domain = os.environ['AUTH0_APP_DOMAIN']
auth0_app_client_id = os.environ['AUTH0_APP_CLIENT_ID']
auth0_app_client_secret = os.environ['AUTH0_APP_CLIENT_SECRET']

def get_access_token_by_refresh_token(refresh_token):
    message = ''
    if not refresh_token or not auth0_app_domain:
        message = 'refresh_token is not null'
    
    try:
        url = 'https://' + auth0_app_domain + '/oauth/token'
        data = "grant_type=refresh_token&client_id=" + auth0_app_client_id + "&client_secret=" + auth0_app_client_secret + "&refresh_token=" + refresh_token
        headers = { 'content-type': "application/x-www-form-urlencoded" }
        response = requests.post(url, data=data, headers=headers)
        print(response)

    except Exception as e:
        print(e)
        message = 'system error.'

    return {
            "result_code": '1',
            "message": message
        }

def get_user_by_token(token):
    message = ''
    if not token or not auth0_app_domain:
        message = 'token is not null'
        
    try:
        url = 'https://' + auth0_app_domain + '/userinfo'
        userinfo = requests.get(url, headers={"Authorization": "Bearer " + token}).json()
        if userinfo and userinfo['email_verified']:
            return {
                "result_code": '0',
                "data": userinfo
            }
        else:
            message = 'token error.'
    except Exception as e:
        print(e)
        message = 'system error.'

    return {
            "result_code": '1',
            "message": message
        }
        
def validate_id_token(id_token):
    if not id_token or not auth0_app_domain:
        return {
            "result_code": '1',
            "message": 'idtoken is not null'
        }
        
    message = ''
    try:
        url = 'https://' + auth0_app_domain + '/.well-known/jwks.json'
        jwks_client = PyJWKClient(url)
        headers = jwt.get_unverified_header(id_token)
        signing_key = jwks_client.get_signing_key_from_jwt(id_token)
        
        data = jwt.decode(
            id_token,
            signing_key.key,
            algorithms=[headers.get("alg")],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iat": True,
                "verify_iss": True,
                "verify_aud": False,
            },
        )
    
    except jwt.InvalidTokenError as e:
        message = "InvalidTokenError"
    except jwt.DecodeError as e:
        message = "DecodeError"
    except jwt.InvalidSignatureError as e:
        message = "InvalidSignatureError"
    except jwt.ExpiredSignatureError as e:
        message = "ExpiredSignatureError"
    except jwt.InvalidIssuerError as e:
        message = "InvalidIssuerError"
    except jwt.InvalidIssuedAtError as e:
        message = "InvalidIssuedAtError"
    except Exception as e:
        message = 'パラメータの形式が無効です。'
    
    if message != '':
        return {
            "result_code": '1',
            "message": message
        }
    if 'email' in data:
        return {
            "result_code": '0',
            "data": data
        }
    return {
            "result_code": '1',
            "message": 'パラメータの形式が無効です。'
        }
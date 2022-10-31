import json
import services.rds_utils as RDU
import services.auth0_utils as AU
import models.oauth_token as OauthToken

def lambda_handler(event, context):

    arguments = event.get('arguments')
    refresh_token = arguments.get('refresh_token')

    renewTokenData = AU.get_access_token_by_refresh_token(refresh_token)
    if renewTokenData['result_code'] != '0':
        response = {
            'result_code': '1',
            'data': {},
            'message': renewTokenData['message']
        }
        print(response)
        return response
    
    data = renewTokenData['data']
    access_token = data.get('access_token')
    select = "SELECT * FROM cs_oauth_refresh_token WHERE refresh_token= '" + refresh_token + "'"
    oauthToken = RDU.fetchOne(select)
    if oauthToken.get('user_id') and access_token:
         OauthToken.insertAccessToken(access_token, oauthToken.get('user_id'))

    response = {
            'result_code': '0',
            'data': data,
        }
    print(response)
    return response
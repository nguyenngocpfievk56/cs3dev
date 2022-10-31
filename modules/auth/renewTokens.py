import json

import services.auth0_utils as AU

def lambda_handler(event, context):

    arguments = event.get('arguments')
    refresh_token = arguments.get('refresh_token')

    user_data = AU.get_access_token_by_refresh_token(refresh_token)
    print(user_data)

    response = {
            'result_code': '0',
            'data': {},
        }
    return response
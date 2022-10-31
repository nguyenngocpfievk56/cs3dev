import json
import uuid

import services.auth0_utils as AU
import services.rds_utils as RU
import models.oauth_token as OauthToken
from datetime import datetime,timedelta
import pytz

tokyoTz = pytz.timezone("Asia/Tokyo")
TODAY = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')


def lambda_handler(event, context):

    arguments = event.get('arguments')
    token = arguments.get('id_token')
    
    user_token = OauthToken.getUserByAccessToken(token)
    print(user_token)
    if user_token and str(user_token['expires']) < TODAY:
        response = {
            'result_code': '1',
            'data': {},
            'message': 'token expires.'
        }
        print(response)
        return response
    elif user_token:
        dataUser = {
            'id' : int(user_token['user_id']),
            'email' : user_token['email'],
            'nickname' : user_token['nickname']
        }
        response = {
            'result_code': '0',
            'data': dataUser
        }
        print(response)
        return response
        
    user_data = AU.get_user_by_token(token)
    if user_data['result_code'] != '0':
        response = {
            'result_code': '1',
            'data': {},
            'message': user_data['message']
        }
        print(response)
        return response

    userResult = user_data['data']
    email = userResult.get('email')
    select = "SELECT id,nickname,email FROM cs_user WHERE email= '" + email + "'"
    userRow = RU.fetchOne(select)

    if userRow.get('email'):
        OauthToken.insertAccessToken(token, userRow.get('id'))
        response = {
            'result_code': '0',
            'data':userRow
        }
        print(response)
        return response
    
    sql = "INSERT INTO `cs_user` (`email`, `passwd`, `mail_magazine_type`, `nickname`, `profile_img`, `created`, `modified`) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    val = (userResult.get('email'), uuid.uuid4(), '1', userResult.get('nickname'), userResult.get('picture'), TODAY, TODAY, )
    rowId = RU.insertOne(sql, val)
    OauthToken.insertAccessToken(token, rowId)
    if rowId:
        select = "SELECT id,nickname,email FROM cs_user WHERE id= '" + rowId + "'"
        userRow = RU.fetchOne(select)
        
    response = {
        'result_code': '0',
        'data': userRow
    }
    print(response)
    return response

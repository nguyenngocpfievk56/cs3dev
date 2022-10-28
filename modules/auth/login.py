import json
import uuid

import services.auth0_utils as AU
import services.rds_utils as RU
from datetime import datetime,timedelta
import pytz
import const
tokyoTz = pytz.timezone("Asia/Tokyo")
TODAY = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')


def lambda_handler(event, context):
    arguments = event.get('arguments')
    id_token = arguments.get('id_token')

    user_data = AU.validate_id_token(id_token)
    if user_data['result_code'] != const.RESULT_CODE_SUCCESS:
        response = {
            'result_code': const.RESULT_CODE_ERROR,
            'data': '{}',
            'message': user_data['message']
        }
        return response

    userResult = user_data['data']
    email = userResult.get('email')
    select = "SELECT id,nickname,email FROM cs_user WHERE email= '" + email + "'"
    userRow = RU.fetchOne(select)

    if userRow.get('email'):
        response = {
            'result_code': const.RESULT_CODE_SUCCESS,
            'data':userRow
        }
        return response

    sql = "INSERT INTO `cs_user` (`email`, `passwd`, `mail_magazine_type`, `nickname`, `profile_img`, `created`, `modified`) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    val = (userResult.get('email'), uuid.uuid4(), '1', userResult.get('nickname'), userResult.get('picture'), TODAY, TODAY, )
    rowId = RU.insertUpdate(sql, val)
    if rowId:
        select = "SELECT id,nickname,email FROM cs_user WHERE id= '" + rowId + "'"
        userRow = RU.fetchOne(select)

    response = {
        'result_code': const.RESULT_CODE_SUCCESS,
        'data': userRow
    }
    return response

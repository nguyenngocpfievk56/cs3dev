import services.rds_utils as RDU
from datetime import datetime
import models.user_mute as UserMute
import pytz
tokyoTz = pytz.timezone("Asia/Tokyo")

TODAY = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')

def lambda_handler(event, context):
    # TODO implement
    arguments = event.get('arguments')
    user_id = arguments.get('user_id')
    mute_user_id = arguments.get('mute_user_id')

    if not user_id or not mute_user_id or user_id == mute_user_id:
       return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "データが不正です"
            }
        }
    if not UserMute.isMuting(user_id, mute_user_id):
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "フォローしていません"
            }
        }
    user_mute = UserMute.getUserMutingRow(user_id, mute_user_id)
    if user_mute:
        sql = "UPDATE `cs_user_mute` SET `deleted` = %s WHERE `id` = %s"
        val = (TODAY, user_mute.get('id'))
        RDU.insertUpdate(sql, val)
    return {
        'result_code': 0
    }
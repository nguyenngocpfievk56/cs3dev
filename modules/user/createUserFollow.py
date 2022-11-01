import services.rds_utils as RDU
from datetime import datetime
import models.user_follow as UserFollow
import pytz
tokyoTz = pytz.timezone("Asia/Tokyo")

TODAY = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')

def lambda_handler(event, context):
    # TODO implement
    arguments = event.get('arguments')
    user_id = arguments.get('user_id')
    following_user_id = arguments.get('following_user_id')

    if not user_id or not following_user_id or user_id == following_user_id:
       return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "データが不正です"
            }
        }
    if UserFollow.isFollowing(user_id, following_user_id):
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "既にフォローしています"
            }
        }
    user_follow = UserFollow.getUserFollowRow(user_id, following_user_id)
    if user_follow:
        sql = "UPDATE `cs_user_follow` SET `deleted` = %s WHERE `id` = %s"
        val = (None, user_follow.get('id'))
    else:
        sql = "INSERT INTO `cs_user_follow` (`user_id`, `following_user_id`, `created`, `modified`) VALUES(%s, %s, %s, %s)"
        val = (user_id, following_user_id, TODAY, TODAY)
    RDU.insertUpdate(sql, val)
    return {
        'result_code': 0
    }
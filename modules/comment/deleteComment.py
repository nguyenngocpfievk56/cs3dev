import services.rds_utils as RDU
from datetime import datetime
import models.entry as Entry
import models.entry_comment as EntryComment
import pytz
tokyoTz = pytz.timezone("Asia/Tokyo")

TODAY = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')

def lambda_handler(event, context):
    # TODO implement
    arguments = event.get('arguments')
    id = arguments.get('id')
    user_id = arguments.get('user_id')

    if not user_id:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "user_id not existed"
            }
        }

    comment = EntryComment.getCommentById(id)
    if not comment:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "entry not existed"
            }
        }
    sql = "UPDATE `cs_entry_comment` SET `deleted` = %s, `modified` = %s WHERE `id` = %s"
    val = (TODAY, TODAY, id)
    RDU.insertUpdate(sql, val)

    if comment['comment_id']:
        EntryComment.doUpdateComment(comment['entry_id'], id)
    else:
        Entry.doUpdateComment(comment['entry_id'])


    return {
        'result_code': 0,
    }
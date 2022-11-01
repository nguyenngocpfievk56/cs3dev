import json
import services.rds_utils as RDU
import models.entry as Entry
import models.clip as Clip
from datetime import datetime
import pytz
tokyoTz = pytz.timezone("Asia/Tokyo")

TODAY = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')


def lambda_handler(event, context):
    # TODO implement
    arguments = event.get('arguments')
    entry_id = arguments.get('entry_id')
    user_id = arguments.get('user_id')
    url = arguments.get('url')

    if not user_id:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "には、ログインが必要です。"
            }
        }

    entry = Entry.getEntryById(entry_id)
    if not entry:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "entry not existed"
            }
        }

    isClip = Clip.isClipped(url, user_id)
    if isClip:
        sql = "UPDATE `cs_clip` SET `deleted` = %s, `modified` = %s WHERE `url` = %s AND user_id = %s"
        val = (TODAY, TODAY, str(url), str(user_id))
        RDU.insertUpdate(sql, val)
        return {
            'result_code': 0
        }
    else:
        return {
                'result_code': 1,
                "error": {
                    "error_code": "UXD_123",
                    "error_message": "clip not existed"
                }
            }

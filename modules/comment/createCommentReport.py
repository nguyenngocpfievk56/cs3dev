import services.rds_utils as RDU
from datetime import datetime
import pytz
tokyoTz = pytz.timezone("Asia/Tokyo")

TODAY = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')

def lambda_handler(event, context):
    # TODO implement
    arguments = event.get('arguments')
    user_id = arguments.get('user_id')
    target_id = arguments.get('comment_id')
    target_table = arguments.get('target_table')
    violate_type = arguments.get('violate_type')
    violate_detail = arguments.get('violate_detail')
    url = arguments.get('url')

    if not user_id:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "user_id not existed"
            }
        }
    if not violate_type:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "violate_type empty"
            }
        }

    if not target_id:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "target_id empty"
            }
        }
    if not target_table: target_table = 'EntryComment'
    sql = "INSERT INTO `cs_report` (`user_id`, `target_id`, `target_table`, `url`, `violate_type`, `violate_detail`, `created`, `modified`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (user_id, target_id, target_table, url, violate_type, violate_detail, TODAY, TODAY)
    RDU.insertUpdate(sql, val)

    return {
        'result_code': 0,
    }
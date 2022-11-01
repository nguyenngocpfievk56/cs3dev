import json
import sys
import services.rds_utils as RDU
from datetime import datetime
import models.entry as Entry
import models.tags as Tags
import models.entry_spot as Spot
import pytz
tokyoTz = pytz.timezone("Asia/Tokyo")

TODAY = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')

def lambda_handler(event, context):
    # TODO implement
    arguments = event.get('arguments')
    entry_id = arguments.get('id')
    user_id = arguments.get('user_id')

    if not user_id:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "user_id not existed"
            }
        }

    entryRow = Entry.getEntryById(entry_id)
    if not entryRow:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "entry not existed"
            }
        }

    sql = "UPDATE `cs_entry` SET `deleted` = %s, `modified` = %s WHERE `id` = %s"
    val = (TODAY, TODAY, entryRow['id'])
    RDU.insertUpdate(sql, val)

    Tags.delHasTagsByEntryId(entryRow['id'])
    Spot.delSpotByEntryId(entryRow['id'])

    return {
        'result_code': 0,
        'data': entryRow['id']
    }
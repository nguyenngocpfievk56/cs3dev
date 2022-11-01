import json
import sys
import services.rds_utils as RDU
from datetime import datetime
import models.module as Module
import models.reaction as Reaction
import models.entry_plus as EntryPlus
import models.entry as Entry
import pytz
tokyoTz = pytz.timezone("Asia/Tokyo")

TODAY = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')


def lambda_handler(event, context):
    # TODO implement
    arguments = event.get('arguments')
    entry_id = arguments.get('entry_id')
    user_id = arguments.get('user_id')

    entry = Entry.getEntryById(entry_id)

    if not user_id:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "user_id not existed"
            }
        }

    if not entry:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "entry not existed"
            }
        }

    entry_plus = EntryPlus.getEntryPlus(entry_id, user_id)
    if entry_plus:
        sql = "UPDATE `cs_entry_plus` SET `deleted` = %s, `modified` = %s WHERE `id` = %s"
        val = (TODAY, TODAY, entry_plus['id'])
        RDU.insertUpdate(sql, val)
    else:
        return {
            'result_code': 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "user not reaction"
            }
        }

    sql = "UPDATE `cs_entry` SET `num_good` = %s, `modified` = %s WHERE `id` = %s"
    num_good = EntryPlus.getCountEntryPlus(entry['id'])
    val = (str(num_good), TODAY, str(entry['id']))
    RDU.insertUpdate(sql, val)

    module = Module.getModuleById(entry['module_id']) if entry['module_id'] else None
    reaction_ids = None
    if module:  reaction_ids = module['reaction_ids']
    response_body = {}
    response_body['reactions'] = {}
    response_body['reactions']['total'] = num_good

    response_body['reactions']["items"] = Reaction.getOptionReactions(reaction_ids, entry['id'])
    response_body['actionStatus'] = {}
    response_body['actionStatus']['reaction'] = None
    print(response_body)
    return {
        'result_code': 0,
        'data': response_body
    }
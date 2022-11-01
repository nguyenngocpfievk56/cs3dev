import json
import sys
import services.rds_utils as RDU
from datetime import datetime
import models.entry as Entry
import models.module as Module
import models.entry_comment as EntryComment
import models.entry_comment_plus as EntryCommentPlus
import models.reaction as Reaction
import pytz
tokyoTz = pytz.timezone("Asia/Tokyo")

TODAY = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')

def lambda_handler(event, context):
    # TODO implement
    arguments = event.get('arguments')
    comment_id = arguments.get('comment_id')
    user_id = arguments.get('user_id')

    if not user_id:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "user_id not existed"
            }
        }

    comment = EntryComment.getEntryById(comment_id)
    if not comment:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "entry not existed"
            }
        }
    entry_comment_plus = EntryCommentPlus.getEntryCommentPlus(comment.get('entry_id'), comment.get('id') , user_id)
    if entry_comment_plus:
        sql = "UPDATE `cs_entry_comment_plus` SET `deleted` = %s, `modified` = %s WHERE `id` = %s"
        val = (TODAY, TODAY, entry_comment_plus['id'])
        RDU.insertUpdate(sql, val)
    else:
        return {
            'result_code': 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "user not reaction"
            }
        }
    sql = "UPDATE `cs_entry_comment` SET `num_good` = %s, `modified` = %s WHERE `id` = %s"
    num_good = EntryCommentPlus.getCountEntryCommentPlus(comment.get('entry_id'), comment.get('id'))
    val = (num_good, TODAY, str(comment.get('id')))
    RDU.insertUpdate(sql, val)
    entry = Entry.getEntryById(comment.get('entry_id'))
    module = Module.getModuleById(entry.get('module_id')) if entry.get('module_id') else None
    reaction_ids = None
    if module:  reaction_ids = module['reaction_ids']
    response_body = {}
    response_body['reactions'] = {}
    response_body['reactions']['total'] = num_good
    response_body['reactions']["items"] = Reaction.getOptionReactions(reaction_ids, comment.get('entry_id'), comment.get('id'), True)
    response_body['actionStatus'] = {}
    response_body['actionStatus']['reaction'] = None
    return {
        'result_code': 0,
        'data': response_body
    }
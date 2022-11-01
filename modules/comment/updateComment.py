import services.rds_utils as RDU
from datetime import datetime
import models.entry as Entry
import models.module as Module
import models.entry_comment as EntryComment
import pytz
tokyoTz = pytz.timezone("Asia/Tokyo")

TODAY = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')

def lambda_handler(event, context):
    # TODO implement
    arguments = event.get('arguments')
    id = arguments.get('id')
    description = arguments.get('description')
    comment_img = arguments.get('comment_img')
    access_token = arguments.get('access_token')
    user_id = 1

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
    entry = Entry.getEntryById(comment.get('entry_id'))
    img = None
    img2 = None
    if comment_img:
        images = comment_img.split(",")
        if images and images[0]: img = images[0]
        if images and images[1]: img2 = images[1]
    sql = "UPDATE `cs_entry_comment` SET `description` = %s, `img` = %s, `img2` = %s, `modified` = %s WHERE `id` = %s"
    val = (description, img, img2, TODAY, id)
    RDU.insertUpdate(sql, val)

    response_body = {}

    module = Module.getModuleById(entry.get('module_id')) if entry.get('module_id') else None
    reaction_ids = None
    if module:
        reaction_ids = module['reaction_ids']

    if comment['comment_id']:
        options = {
            "reaction_ids": reaction_ids,
            "user_id": user_id,
            "is_child_comment": True
        }
        EntryComment.doUpdateComment(comment['entry_id'], id)
    else:
        options = {
            "reaction_ids": reaction_ids,
            "user_id": user_id
        }
        Entry.doUpdateComment(comment['entry_id'])

    response_body['item'] = EntryComment.getOptionEntryCommentResponse(comment, options)

    return {
        'result_code': 0,
        'data': response_body
    }
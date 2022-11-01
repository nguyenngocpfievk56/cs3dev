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
    entry_id = arguments.get('entry_id')
    comment_id = arguments.get('comment_id')
    description = arguments.get('description')
    comment_img = arguments.get('comment_img')
    access_token = arguments.get('access_token')

    user_id = 1
    entry = Entry.getEntryById(entry_id)
    if not user_id:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "user_id not existed"
            }
        }

    if not description:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "description empty"
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
    img = None
    img2 = None
    if comment_img:
        images = comment_img.split(",")
        if images and images[0]: img = images[0]
        if images and images[1]: img2 = images[1]

    sql = "INSERT INTO `cs_entry_comment` (`entry_id`, `user_id`, `description`, `status`, `img`, `img2`, `comment_id`, `created`, `modified`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (str(entry_id), str(user_id), description, EntryComment.STATUS_NEW, img, img2, comment_id, TODAY, TODAY)
    rowId = RDU.insertUpdate(sql, val)
    response_body = {}
    if rowId:
        module = Module.getModuleById(entry.get('module_id')) if entry.get('module_id') else None
        reaction_ids = None
        if module:
            reaction_ids = module['reaction_ids']

        if comment_id:
            options = {
                "reaction_ids": reaction_ids,
                "user_id": user_id,
                "is_child_comment": True
            }
            EntryComment.doUpdateComment(entry_id, comment_id)
        else:
            options = {
                "reaction_ids": reaction_ids,
                "user_id": user_id
            }
            Entry.doUpdateComment(entry_id)

        item = EntryComment.getCommentById(rowId)
        response_body = EntryComment.getOptionEntryCommentResponse(item, options)

    return {
        'result_code': 0,
        'data': response_body
    }
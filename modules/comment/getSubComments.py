import models.entry_comment as EntryComment
import models.module as Module

def lambda_handler(event, context):
    # TODO implement
    arguments = event.get('arguments')
    entry_id = arguments.get('entry_id')
    comment_id = arguments.get('comment_id')
    module_id = arguments.get('module_id')
    limit = arguments.get('limit')
    currentPage = arguments.get('currentPage')
    user_id = arguments.get('user_id')

    sort = arguments.get('sort')
    if not limit: limit = 3
    if not currentPage: currentPage = 1
    offset = (int(currentPage) - 1) * int(limit)

    if not comment_id:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "comment_id not existed"
            }
        }

    module = Module.getModuleById(module_id) if module_id else None
    reaction_ids = None
    if module:
        reaction_ids = module['reaction_ids']

    result = EntryComment.getChildComments(comment_id, sort, limit, offset)
    total = EntryComment.countComment(entry_id, comment_id)

    comments = {}
    comments["total"] = total
    comments["sort"] = str(sort)
    comments["currentPage"] = int(currentPage)
    comments["limit"] = int(limit)
    comments["items"] = []
    options = {
        "reaction_ids": reaction_ids,
        "user_id": user_id,
        "is_child_comment": True
    }
    if result:
        for item in result:
            comment = EntryComment.getOptionEntryCommentResponse(item, options)
            comments['items'].append(comment)

    response = {
        "result_code": 0,
        "data": comments
    }

    return response

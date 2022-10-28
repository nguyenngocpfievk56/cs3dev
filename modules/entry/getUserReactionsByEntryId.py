import models.entry_plus as EntryPlus

def lambda_handler(event, context):
    # TODO implement
    arguments = event.get('arguments')
    entry_id = arguments.get('entry_id')

    limit = arguments.get('limit')
    currentPage = arguments.get('currentPage')

    if not limit: limit = 10
    if not currentPage: currentPage = 1
    offset = (int(currentPage) - 1) * int(limit)

    if not entry_id:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "entry_id not existed"
            }
        }

    result = EntryPlus.getEntryPlus(entry_id, limit, offset)
    total = EntryPlus.getCountEntryPlus(entry_id)

    entryPlus = {}
    entryPlus["total"] = total
    entryPlus["currentPage"] = int(currentPage)
    entryPlus["limit"] = int(limit)
    entryPlus["user_reactions"] = []

    if result:
        for row in result:
            reactions = {}
            item = {}
            if row['reaction_id'] is not None and row['reaction_name'] is not None:
                reactions['id'] = row['reaction_id']
                reactions['caption'] = row['reaction_name']
                reactions['img'] = row['reaction_img']
            
            item['id'] = row['id']
            item['nickname'] = row['nickname']
            item['profile_img'] = row['profile_img']
            item['introduction'] = row['introduction']
            item['reaction'] = reactions
            entryPlus['user_reactions'].append(item)

    response = {
        "result_code": 0,
        "data": entryPlus
    }

    return response

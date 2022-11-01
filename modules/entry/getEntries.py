import models.entry as Entry

def lambda_handler(event, context):
    arguments = event.get('arguments')
    limit = arguments.get('limit')
    currentPage = arguments.get('currentPage')
    access_token = arguments.get('access_token')
    user_id = arguments.get('user_id')

    user_id = 1
    input = {}
    sort = arguments.get('sort')
    input['sort'] = Entry.sortCondition(sort)
    if not limit: limit = 10
    if not currentPage or currentPage < 1: currentPage = 1
    offset = (int(currentPage) - 1) * int(limit)

    result = Entry.getEntries(input, limit, offset)
    total = Entry.getTotalEntries(input)

    entries = {}
    entries["total"] = total
    entries["sort"] = str(sort)
    entries["currentPage"] = int(currentPage)
    entries["limit"] = int(limit)
    entries["items"] = []

    if result:
        for item in result:
            entry = Entry.getOptionEntryResponse(item, user_id)
            entries['items'].append(entry)

    response = {
        "result_code": 0,
        "data": entries
    }

    return response
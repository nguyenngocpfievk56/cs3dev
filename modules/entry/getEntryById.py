import models.entry as Entry

def lambda_handler(event, context):
    arguments = event.get('arguments')
    entry_id = arguments.get('id')
    user_id = arguments.get('user_id')

    item = Entry.getEntryById(entry_id)
    if not item:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "entry not existed"
            }
        }

    entry = Entry.getOptionEntryResponse(item, user_id)
    return {
        "result_code": 0,
        "data": entry
    }
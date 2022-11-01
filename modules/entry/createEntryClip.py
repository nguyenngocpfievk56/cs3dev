import json
import models.entry as Entry
import models.clip as Clip

def lambda_handler(event, context):
    arguments = event.get('arguments')
    entry_id = arguments.get('entry_id')
    user_id = arguments.get('user_id')
    url = arguments.get('url')

    if not user_id:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "には、ログインが必要です。"
            }
        }

    entry = Entry.getEntryById(entry_id)
    if not entry:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "entry not existed"
            }
        }
    isClip = Clip.isClipped(url, user_id)
    if isClip:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "entry is clip."
            }
        }

    Clip.insertClip(entry, url, user_id)
    # TODO implement
    return {
        "result_code": 0
    }

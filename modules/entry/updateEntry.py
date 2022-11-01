import json
import re
import services.rds_utils as RDU
import models.entry as Entry
import models.entry_spot as Spot
import models.module as Module
import models.tags as Tags
from datetime import datetime
import pytz
tokyoTz = pytz.timezone("Asia/Tokyo")

NOW = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')

def lambda_handler(event, context):
    arguments = event.get('arguments')

    id = arguments.get('id')
    user_id = arguments.get('user_id')
    module_id = arguments.get('module_id')
    category_l_id = arguments.get('category_l_id')
    images = arguments.get('images')
    description = arguments.get('description')
    caption = arguments.get('caption')
    spot = arguments.get('spot')
    error_params = {}
    module = Module.getModuleById(module_id)

    if id is None:
        error_params['id'] = '入力必須です。'
    if not module:
        error_params['module'] = 'module_id not exist.'
    if user_id is None:
        error_params['user_id'] = '入力必須です。'
    if description is None:
        error_params['description'] = '入力必須です。'
    if images is None:
        error_params['images'] = '入力必須です。'

    if error_params:
        response = {
            "result_code": 1,
            'error_params': error_params,
            "data": {}
        }
        return response

    entryRow = Entry.getEntryById(id)
    if entryRow['id'] is not None:
        sqlUpdate = "UPDATE cs_entry SET modified = %s, caption = %s, description = %s, category_l_id = %s, img = %s WHERE id = '" + str(id) + "'"
        val = (NOW, caption, description, category_l_id, images)
        print(description)
        RDU.insertUpdate(sqlUpdate, val)

        if spot is not None and entryRow['id'] is not None:
            dataPot = json.loads(spot)
            Spot.insertUpdateSpotByEntryId(dataPot, entryRow['id'])

        hashtag_list = Tags.makeHashtag(description)
        print(hashtag_list)
        if entryRow['id'] is not None and len(hashtag_list) > 0:
            Tags.saveTagEntryRelation(entryRow, hashtag_list, Tags.TEXT_HASH_TAG_ON)
    return {
        'result_code': 0,
        'data': entryRow['id']
    }
import json
import services.rds_utils as RDU
import models.entry as Entry
import models.entry_spot as Spot
import models.module as Module
import models.tags as Tags
from datetime import datetime
import pytz
tokyoTz = pytz.timezone("Asia/Tokyo")

NOW = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')
IS_FORMAL = 1

def lambda_handler(event, context):
    arguments = event.get('arguments')

    user_id = arguments.get('user_id')
    module_id = arguments.get('module_id')
    category_l_id = arguments.get('category_l_id')
    images = arguments.get('images')
    description = arguments.get('description')
    caption = arguments.get('caption')
    spot = arguments.get('spot')
    error_params = {}
    module = Module.getModuleById(module_id)

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

    sqlnsert = "INSERT INTO cs_entry (`created`,`modified`,`user_id`,`status`,`is_formal`,`caption`,`description`,`module_id`,`module_type`,`category_l_id`,`img`) VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (NOW, NOW, user_id, Entry.STATUS_NEW, IS_FORMAL, caption, description, module_id, module['type'], category_l_id, images)
    entryId = RDU.insertOne(sqlnsert, val)
    if entryId:
        entryRow = Entry.getEntryById(entryId)
    else:
        return {
            'result_code': 1,
            'data': {}
        }

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
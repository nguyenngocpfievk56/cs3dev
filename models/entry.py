import services.rds_utils as RDU
from datetime import datetime
import models.user as User
import models.module as Module
import models.category_large as CategoryLarge
import models.reaction as Reaction
import models.entry_spot as EntrySpot
import models.user_follow as UserFollow
import models.user_mute as UserMute
import models.entry_plus as EntryPlus
import models.entry_comment as EntryComment
import pytz

tokyoTz = pytz.timezone("Asia/Tokyo")

NOW = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')
STATUS_NEW       = '1'
STATUS_APPROVAL  = '2'

def sortCondition(sort):
    condition = 'created DESC'
    if not sort: return condition
    switcher = {
        "new" : 'created DESC',
        "comment" : 'num_comment DESC',
        "modified" : 'modified DESC',
        "opened" : 'opened DESC',
        "num_view" : 'num_view DESC',
        "num_good" : 'num_good DESC',
        "opened_new" : 'IFNULL(opened, created) DESC'
    }
    return switcher.get(sort, "created DESC")

def getEntries(input, limit = 10, offset = 0):
    query = "SELECT `es`.*, `us`.`profile_img`, `us`.`nickname`, `ess`.`name`, `ess`.`region`, `ess`.`city` "
    query += "FROM `cs_entry` AS `es` INNER JOIN `cs_user` AS `us` ON es.user_id = us.id LEFT JOIN `cs_entry_spot` AS `ess` ON es.id = ess.entry_id "
    query += "WHERE (es.deleted IS NULL) AND (us.deleted IS NULL) AND (ess.deleted IS NULL) AND (es.status in (" + STATUS_NEW + ", " + STATUS_APPROVAL + ")) AND (es.opened is null or es.opened <= '" + str(NOW) + "') AND (es.closed is null or es.closed >= '" + str(NOW) + "')"

    if input.get('module_id'): query += " AND (es.module_id = " + str(input.get('module_id')) + ")"

    if input.get('sort'): query += " ORDER BY es." + str(input.get('sort'))
    if limit:
        if offset: query += " LIMIT " + str(limit) + " OFFSET " + str(offset)
        else: query += " LIMIT " + str(limit)
    return RDU.fetchAll(query)

def getTotalEntries(input):
    query = "SELECT COUNT(`es`.id) as cnt "
    query += "FROM `cs_entry` AS `es` INNER JOIN `cs_user` AS `us` ON es.user_id = us.id LEFT JOIN `cs_entry_spot` AS `ess` ON es.id = ess.entry_id "
    query += "WHERE (es.deleted IS NULL) AND (us.deleted IS NULL) AND (ess.deleted IS NULL) AND (es.status in (" + STATUS_NEW + ", " + STATUS_APPROVAL + ")) AND (es.opened is null or es.opened <= '" + str(NOW) + "') AND (es.closed is null or es.closed >= '" + str(NOW) + "')"

    if input.get('module_id'): query += " AND (es.module_id = " + str(input.get('module_id')) + ")"

    if input.get('sort'): query += " ORDER BY es." + str(input.get('sort'))

    result = RDU.fetchOne(query)

    return result['cnt'] if result else 0

def getEntryById(entry_id):
    if not entry_id: return None

    query ="SELECT * FROM `cs_entry` WHERE (deleted IS NULL) AND (id = " + str(entry_id) + ")"

    return RDU.fetchOne(query)

def getOptionEntryResponse(item, user_id):
    entry = {}
    entry['id'] = item['id']
    entry['description'] = item['description']
    entry['caption'] = item['caption']
    entry['thumbnail'] = item['img_thumbnail']
    entry['curationSource'] = item['sns_type']
    entry["createdTime"] = item['created'].timestamp()
    entry['curationSource'] = item['sns_type']
    entry['comment'] = item['num_comment']
    entry['view'] = item['num_view']
    entry['spot'] = {}
    entry_spot = EntrySpot.getEntrySpotByEntryId(item['id'])
    if entry_spot:
        entry['spot']['name'] = entry_spot['name']
        entry['spot']['region'] = entry_spot['region']
        entry['spot']['city'] = entry_spot['city']
        entry['spot']['country'] = entry_spot['country']
        entry['spot']['street'] = entry_spot['street']
    entry['reactions'] = {}
    entry['reactions']['total'] = item['num_good']
    module = Module.getModuleById(item['module_id'])
    reaction_ids = None
    if module:
        entry['module'] = {}
        entry['module']['id'] = module['id']
        entry['module']['caption'] = module['caption']
        entry['module']['alias'] = module['alias']
        entry['module']['type'] = module['type']
        reaction_ids = module['reaction_ids']
    entry['reactions']["items"] = Reaction.getOptionReactions(reaction_ids, item['id'])
    category_large = CategoryLarge.getCategoryLatgeById(item['category_l_id'])
    if category_large:
        entry['category'] = {}
        entry['category']['id'] = category_large['id']
        entry['category']['caption'] = category_large['title']
        entry['category']['alias'] = category_large['category_l_alias']
        entry['category']['img'] = category_large['img']
    entry["tags"] = item['tag'].split(",") if item['tag'] else []
    entry["medias"] = convertImage(item)
    user = User.getUserById(item['user_id'])
    if user:
        entry['user'] = {}
        entry['user']['id'] = user['id']
        entry['user']['nickname'] = user['nickname']
        entry['user']['profileImg'] = user['profile_img']
        entry['user']['title'] = user['title']
        entry['user']['isAdmin'] = user['is_admin']
    entry['actionStatus'] = {}
    entry['actionStatus']['reaction'] = EntryPlus.isEntryPlus(item['id'], user_id) if user_id else False
    entry['actionStatus']['follow'] =  UserFollow.isFollowing(user_id, item['user_id']) if user_id else False
    entry['actionStatus']['mute'] =  UserMute.isMuting(user_id, item['user_id']) if user_id else False
    entry['actionStatus']['clip'] =  False
    return entry

def convertImage(item):
    images = []
    if item['img']:
        image = {}
        image['url'] = item['img']
        image['type'] = item['img_type']
        images.append(image)

    if item['img2']:
        image = {}
        image['url'] = item['img2']
        image['type'] = item['img_type2']
        images.append(image)

    if item['img3']:
        image = {}
        image['url'] = item['img3']
        image['type'] = item['img_type3']
        images.append(image)

    if item['img4']:
        image = {}
        image['url'] = item['img4']
        image['type'] = item['img_type4']
        images.append(image)

    if item['img5']:
        image = {}
        image['url'] = item['img5']
        image['type'] = item['img_type5']
        images.append(image)

    return images

def doUpdateComment(entry_id):
    total = EntryComment.countComment(entry_id)
    sql = "UPDATE `cs_entry` SET `num_comment` = %s, `modified` = %s WHERE `id` = %s"
    val = (total, NOW, entry_id)
    RDU.insertUpdate(sql, val)

    return True

def doUpdateNumView(entry_id, num_view):
    sql = "UPDATE `cs_entry` SET `num_view` = %s,`modified` = %s WHERE `id` = %s"
    val = (num_view, NOW, entry_id)
    RDU.insertUpdate(sql, val)

    return True

import services.rds_utils as RDU
from datetime import datetime

def getEntryPlus(entry_id, limit = None, offset = 0):
    if not entry_id or not limit: return None

    query = "SELECT `ep`.*, us.id as user_id, us.nickname as nickname, us.introduction as introduction, us.profile_img as profile_img, rm.reaction_name as reaction_name, us.reaction_img as reaction_img "
    query += "FROM `cs_entry_plus` AS `ep` "
    query += "INNER JOIN `cs_user` AS `us` ON ep.user_id = us.id "
    query += "LEFT JOIN `cs_reaction_master` AS `rm` ON ep.reaction_id = rm.id "
    query += "WHERE (ep.deleted IS NULL) AND (us.deleted IS NULL) AND (ep.entry_id = " + str(entry_id) + ")"

    query += " ORDER BY `ep`.`id` DESC "

    if limit:
        if offset: query += " LIMIT " + str(limit) + " OFFSET " + str(offset)
        else: query += " LIMIT " + str(limit)

    return RDU.fetchAll(query)

def getCountEntryPlus(entry_id, reaction_id = None):
    if not entry_id: return 0
    query = "SELECT COUNT(id) as cnt FROM `cs_entry_plus` WHERE (deleted IS NULL) AND (entry_id =  " + str(entry_id) + ")"
    if reaction_id: query += " AND (reaction_id =  " + str(reaction_id) + ")"

    result = RDU.fetchOne(query)
    return result['cnt'] if result else 0

def getEntryPlus(entry_id, user_id):
    if not entry_id or not user_id: return None
    query = "SELECT * FROM `cs_entry_plus` WHERE (deleted IS NULL) AND (entry_id =  " + str(entry_id) + ") AND (user_id =  " + str(user_id) + ")"

    return RDU.fetchOne(query)

def isEntryPlus(entry_id, user_id):
    result = getEntryPlus(entry_id, user_id)
    if not result: return None
    return result['reaction_id'] if result['reaction_id'] else True

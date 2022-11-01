import services.rds_utils as RDU
from datetime import datetime

def getEntryViewByRow(entry_id, options):
    if not entry_id: return None
    query = "SELECT COUNT(id) as cnt FROM `cs_entry_view` WHERE (deleted IS NULL) AND (entry_id =  " + entry_id + ")"
    if options.get('user_id'): query += " AND (user_id =  " + options.get('user_id') + ")"
    else: query += " AND (ip =  " + options.get('ip') + ")  AND (ua =  " + options.get('ua') + ")"
    return RDU.fetchOne(query)

def getEntryCountByUser(user_id):
    if not user_id: return 0
    query = "SELECT COUNT(id) as cnt FROM `cs_entry_view` WHERE (deleted IS NULL) AND (user_id =  " + user_id + ")"

    result = RDU.fetchOne(query)
    return result['cnt'] if result else 0

def getCount(entry_id):
    if not entry_id: return 0
    query = "SELECT COUNT(id) as cnt FROM `cs_entry_view` WHERE (deleted IS NULL) AND (entry_id =  " + entry_id + ")"

    result = RDU.fetchOne(query)
    return result['cnt'] if result else 0
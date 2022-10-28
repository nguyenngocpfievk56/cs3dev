import services.rds_utils as RDU
from datetime import datetime

def getCountEntryCommentPlus(entry_id, comment_id, reaction_id = None):
    if not entry_id or not comment_id: return 0
    query = "SELECT COUNT(id) as cnt FROM `cs_entry_comment_plus` WHERE (deleted IS NULL) AND (entry_id =  " + str(entry_id) + ") AND (entry_comment_id =  " + str(comment_id) + ")"
    if reaction_id: query += " AND (reaction_id =  " + str(reaction_id) + ")"

    result = RDU.fetchOne(query)
    return result['cnt'] if result else 0

def getEntryCommentPlus(entry_id, comment_id, user_id):
    if not entry_id or not user_id or not comment_id: return None
    query = "SELECT * FROM `cs_entry_comment_plus` WHERE (deleted IS NULL) AND (entry_id =  " + str(entry_id) + ") AND (user_id =  " + str(user_id) + ") AND (entry_comment_id =  " + str(comment_id) + ")"

    return RDU.fetchOne(query)

def isEntryCommentPlus(entry_id, comment_id, user_id):
    result = getEntryCommentPlus(entry_id, comment_id, user_id)
    if not result: return None
    return result['reaction_id'] if result['reaction_id'] else True

import services.rds_utils as RDU
from datetime import datetime

def isFollowing(user_id, following_user_id):
    result = getUserFollowingRow(user_id, following_user_id)
    return True if result else False

def getUserFollowRow(user_id, following_user_id):
    if not following_user_id or not user_id: return None
    query = "SELECT * FROM `cs_user_follow` WHERE (user_id =  " + str(user_id) + ") AND (following_user_id =  " + str(following_user_id) + ")"
    return RDU.fetchOne(query)

def getUserFollowingRow(user_id, following_user_id):
    if not following_user_id or not user_id: return None
    query = "SELECT * FROM `cs_user_follow` WHERE (deleted IS NULL) AND (user_id =  " + str(user_id) + ") AND (following_user_id =  " + str(following_user_id) + ")"
    return RDU.fetchOne(query)

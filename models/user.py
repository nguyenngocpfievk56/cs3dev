import services.rds_utils as RDU
from datetime import datetime

def getUserById(user_id):
    if not user_id: return None

    query ="SELECT * FROM `cs_user` WHERE (deleted IS NULL) AND (id = " + str(user_id) + ")"

    return RDU.fetchOne(query)
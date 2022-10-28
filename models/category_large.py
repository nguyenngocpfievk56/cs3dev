import services.rds_utils as RDU
from datetime import datetime

def getCategoryLatgeById(category_l_id):
    if not category_l_id: return None

    query ="SELECT * FROM `cs_category_large` WHERE (deleted IS NULL) AND (id = " + str(category_l_id) + ")"

    return RDU.fetchOne(query)

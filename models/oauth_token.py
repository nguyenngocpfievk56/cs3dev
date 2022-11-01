import services.rds_utils as RDU
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
tokyoTz = pytz.timezone("Asia/Tokyo")
today = datetime.now(tokyoTz)

def getUserByAccessToken(access_token):
    if not access_token: return None

    query  = "SELECT `oat`.*, us.id as user_id, us.email as email, us.nickname as nickname "
    query += "FROM `cs_oauth_access_token` AS `oat` "
    query += "INNER JOIN `cs_user` AS `us` ON oat.user_id = us.id "
    query += "WHERE (oat.deleted IS NULL) AND (us.deleted IS NULL) AND (oat.access_token = '" + str(access_token) + "')"

    return RDU.fetchOne(query)
    
def insertAccessToken(access_token, user_id, expires = None):
    if not access_token: return None
    
    if expires is None: expires = (today + relativedelta(days = 1)).strftime('%Y-%m-%d %H:%M:%S')
    date_time = today.strftime('%Y-%m-%d %H:%M:%S')
    sqlInsert = "INSERT INTO cs_oauth_access_token (`created`,`modified`,`access_token`,`user_id`,`expires`) VALUE (%s,%s,%s,%s,%s)"
    val = (date_time, date_time, access_token, user_id, expires)
    RDU.insertUpdate(sqlInsert, val)

def insertRefreshToken(refresh_token, user_id, expires = None):
    if not refresh_token: return None
    
    if expires is None: expires = (today + relativedelta(days = 30)).strftime('%Y-%m-%d %H:%M:%S')
    date_time = today.strftime('%Y-%m-%d %H:%M:%S')
    sqlInsert = "INSERT INTO cs_oauth_refresh_token (`created`,`modified`,`refresh_token`,`user_id`,`expires`) VALUE (%s,%s,%s,%s,%s)"
    val = (date_time, date_time, refresh_token, user_id, expires)
    RDU.insertUpdate(sqlInsert, val)
import hashlib
import services.rds_utils as RDU
from datetime import datetime
import pytz
tokyoTz = pytz.timezone("Asia/Tokyo")
NOW = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')

def insertClip(entryRow, url, user_id):
    if not entryRow or not url or not user_id: return None

    short_url = createShortUrl(url)
    if entryRow['img_thumbnail'] is not None: img = entryRow['img_thumbnail']
    elif entryRow['img'] is not None: img = entryRow['img']
    else: img = entryRow['img'] = ''

    sqlspot = "INSERT INTO cs_clip (`created`,`modified`,`entry_id`,`user_id`,`url`,`short_url`,`caption`,`img`) VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (NOW, NOW, entryRow['id'], user_id, url, short_url, entryRow['caption'], img)
    return RDU.insertUpdate(sqlspot, val)

def isClipped(url, user_id):
    if not url or not user_id: return None
    query = "SELECT * FROM `cs_clip` WHERE (deleted IS NULL) AND (user_id =  " + str(user_id) + ") AND (url =  " + str(url) + ")"

    result = RDU.fetchOne(query)
    return True if result else False

def createShortUrl(url):
    result = hashlib.md5(url.encode())
    return result.hexdigest()[:10]
import re
import services.rds_utils as RDU
import models.entry as Entry
from datetime import datetime,timedelta
import pytz
tokyoTz = pytz.timezone("Asia/Tokyo")
NOW = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')

TEXT_HASH_TAG_ON = 1
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

def makeHashtag(description):
    if not description:
        return None
    regex = "#(\w+)"
    hashtag_list = re.findall(regex, description)
    return hashtag_list

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext
  
def saveTagEntryRelation(entryItem, tags, text_flg):
    tags = list(set(tags))
    if entryItem['id'] is not None and len(tags) > 0:
        
        delHasTagsByEntryId(entryItem['id'])
        for tag in tags:
            tag = cleanhtml(tag)
            select = "SELECT id,caption FROM cs_tag WHERE caption= '" + str(tag) + "' and deleted is null"
            tagRow = RDU.fetchOne(select)
            if not tagRow:
                sqltag = "INSERT INTO cs_tag (`created`,`modified`,`caption`,`user_id`,`status`) VALUE (%s,%s,%s,%s,%s)"
                val = (NOW, NOW, tag, entryItem['user_id'], Entry.STATUS_APPROVAL)
                tagId = RDU.insertOne(sqltag, val)
            else:
                tagId = tagRow.get('id')
            if tagId:
                sqlhastag = "INSERT INTO cs_entry_has_tag (`created`,`modified`,`entry_id`,`tag_id`,`is_text_hashtag`) VALUE (%s,%s,%s,%s,%s)"
                val = (NOW, NOW, entryItem['id'], tagId, text_flg)
                RDU.insertOne(sqlhastag, val)
    return True

def delHasTagsByEntryId(entry_id):
    if not entry_id:
        return None
        
    sqlHasTag = "UPDATE `cs_entry_has_tag` SET `deleted` = %s, `modified` = %s WHERE `entry_id` = %s"
    val = (NOW, NOW, str(entry_id))
    
    return RDU.insertUpdate(sqlHasTag, val)

                
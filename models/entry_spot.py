import services.rds_utils as RDU
from datetime import datetime
import pytz
tokyoTz = pytz.timezone("Asia/Tokyo")
NOW = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')

def getEntrySpotByEntryId(entry_id):
    if not entry_id: return None

    query ="SELECT * FROM `cs_entry_spot` WHERE (deleted IS NULL) AND (entry_id = " + str(entry_id) + ")"

    return RDU.fetchOne(query)

def insertUpdateSpotByEntryId(dataPot, entry_id):
    if not dataPot or not entry_id: return None
    google_place_id = dataPot.get('google_place_id')
    name = dataPot.get('name')
    lat = dataPot.get('lat')
    lng = dataPot.get('lng')
    country = dataPot.get('country')
    region = dataPot.get('region')
    city = dataPot.get('city')
    street = dataPot.get('street')

    spotRow = getEntrySpotByEntryId(id)
    
    if spotRow['id'] is not None:
        sqlspot = "UPDATE cs_entry_spot SET `modified` = %s,`google_place_id` = %s, `name` = %s, `lat` = %s,`lng` = %s,`country` = %s,`region` = %s,`city` = %s,`street` = %s WHERE id = '" + str(spotRow['id']) + "'"
        val = (NOW, google_place_id, name, lat, lng, country, region, city, street)
        RDU.insertUpdate(sqlspot, val)
    else:
        sqlspot = "INSERT INTO cs_entry_spot (`created`,`modified`,`entry_id`,`google_place_id`,`name`,`lat`,`lng`,`country`,`region`,`city`,`street`) VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (NOW, NOW, entry_id, google_place_id, name, lat, lng, country, region, city, street)
        RDU.insertUpdate(sqlspot, val)

def delSpotByEntryId(entry_id):
    if not entry_id:
        return None
        
    sqlSopt = "UPDATE `cs_entry_spot` SET `deleted` = %s, `modified` = %s WHERE `entry_id` = %s"
    val = (NOW, NOW, str(entry_id))

    return RDU.insertUpdate(sqlSopt, val)
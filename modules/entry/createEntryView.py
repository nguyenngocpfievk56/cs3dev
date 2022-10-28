import services.rds_utils as RDU
from datetime import datetime
import models.entry_view as EntryView
import models.entry as Entry
import pytz
tokyoTz = pytz.timezone("Asia/Tokyo")

TODAY = datetime.now(tokyoTz).strftime('%Y-%m-%d %H:%M:%S')


def lambda_handler(event, context):
    # TODO implement
    arguments = event.get('arguments')
    entry_id = arguments.get('entry_id')
    user_id = arguments.get('user_id')
    ip = arguments.get('ip')
    ua = arguments.get('ua')

    entry = Entry.getEntryById(entry_id)
    if not entry_id:
        return {
            "result_code": 1,
            "error": {
                "error_code": "UXD_123",
                "error_message": "entry not existed"
            }
        }
    options = {
        "user_id": user_id,
        "ip": ip,
        "ua": ua
    }
    entry_view = EntryView.getEntryViewByRow(entry_id, options)
    if user_id:
        if entry_view:
            sql = "UPDATE `cs_entry_view` SET `modified` = %s WHERE `id` = %s"
            val = (TODAY, entry_view.get('id'))
            RDU.insertUpdate(sql, val)
        else:
            sql = "INSERT INTO `cs_entry_view` (`entry_id`, `user_id`, `ip`, `ua`, `created`, `modified`) VALUES(%s, %s, %s, %s, %s, %s)"
            val = (entry_id, user_id, ip, ua, TODAY, TODAY)
            RDU.insertUpdate(sql, val)

            num_view = 1 if entry.get('num_view') else int(entry.get('num_view')) + 1
            Entry.doUpdateNumView(entry_id, num_view)
    else:
        if not entry_view:
            sql = "INSERT INTO `cs_entry_view` (`entry_id`, `ip`, `ua`, `created`, `modified`) VALUES(%s, %s, %s, %s, %s)"
            val = (entry_id, ip, ua, TODAY, TODAY)
            RDU.insertUpdate(sql, val)
            num_view = 1 if entry.get('num_view') else int(entry.get('num_view')) + 1
            Entry.doUpdateNumView(entry_id, num_view)

    return {
        'result_code': 0,
    }
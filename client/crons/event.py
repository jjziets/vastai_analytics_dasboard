from lib.database import Database
import time
import settings
from lib.sys import log

def run():
    db = Database()

    values = []

    for key, item in enumerate(settings.args.values.split(",")):
        if len(item) > 45:
            item = item[0:44]

        values.append(item)

    db.insert_event({
        "time": settings.args.time,
        "name": settings.args.name,
        "val1": values[0] if len(values) >= 1 else None,
        "val2": values[1] if len(values) >= 2 else None,
        "val3": values[2] if len(values) >= 3 else None,
        "val4": values[3] if len(values) >= 4 else None
    })

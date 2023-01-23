import json
import requests
import settings
from lib.vast import Vast
from lib.sys import log
from models import vast as models
import os
import time
from lib.database import Database
from lib.decorators import set_interval


def run():
    vast = Vast(username=settings.VAST_USERNAME, password=settings.VAST_PASSWORD)
    while vast == None:
        time.sleep(1)
        vast = Vast(username=settings.VAST_USERNAME, password=settings.VAST_PASSWORD)
    account = vast.get_account()
    while account == None:
        time.sleep(1)
        account = vast.get_account()
    machine = vast.get_machine(id=settings.VAST_MACHINE_ID)
    while machine == None:
        time.sleep(1)
        machine = vast.get_machine(id=settings.VAST_MACHINE_ID)
    machine.instances = vast.get_instances(machine_id=settings.VAST_MACHINE_ID)
    while machine.instances == None:
        time.sleep(1)
        machine.instances = vast.get_instances(machine_id=settings.VAST_MACHINE_ID)

    db = Database()
    _time = int(time.time())

    db.insert_machine(_time, {
        "account_credit": account.current['total'],
        "reliability": machine.reliability2,
        "rentals_stored": 0 if machine.current_rentals_resident == None else machine.current_rentals_resident,
        "rentals_on_demand": 0 if machine.current_rentals_running_on_demand == None else machine.current_rentals_running_on_demand,
        "rentals_bid": 0 if machine.current_rentals_running == None or machine.current_rentals_running_on_demand == None else machine.current_rentals_running - machine.current_rentals_running_on_demand,
        "earn_hour": 0 if machine.earn_hour == None else machine.earn_hour,
        "hostname": machine.hostname,
        "earn_day": 0 if machine.earn_day == None else machine.earn_day,
        "verification": machine.verification
    })

    for key, instance in enumerate(machine.instances):
        db.insert_instance(_time, {
            "instance_id": key,
            "earning": 0 if instance.next_state == "running" else instance.min_bid
        })

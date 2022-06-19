from lib.database import Database
from lib.exec import exec
import psutil
import time
import GPUtil
from lib.decorators import set_interval
import settings


def run():
    db = Database()
    _time = int(time.time())
    cpu_usage = psutil.cpu_percent()
    disk_space = psutil.disk_usage('/var/lib/docker')
    disk_usage = psutil.disk_io_counters(perdisk=False)
    #    network_usage = psutil.net_io_counters(pernic=True)["docker0"]
    network_usage = psutil.net_io_counters(pernic=True)
    #    cputemp = 0 if open("/sys/class/thermal/thermal_zone0/temp",'r').readlines() == None else open("/sys/class/thermal/thermal_zone0/temp",'r').readlines()
    #    temperatures2 = float(cputemp[0])/1000
    networksum = 0

    def get_average(items):
        items = [item.current for item in items]
        return sum(items) / len(items)

    def get_CPUTemps():
        testCPUTemp = psutil.sensors_temperatures()
        if 'coretemp' in testCPUTemp :
            testCPUTemp = get_average(testCPUTemp['coretemp'])
            return testCPUTemp
        if 'k10temp' in testCPUTemp :
            testCPUTemp = (testCPUTemp.get('k10temp')[0][1])
            return testCPUTemp
        testCPUTemp = open("/sys/class/thermal/thermal_zone0/temp", 'r').readlines()
        if testCPUTemp != None:
            testCPUTemp = float(testCPUTemp[0]) / 1000
            return testCPUTemp
        return 0

    db.insert_hardware(_time, {
        "component": "ram",
        "hw_id": None,
        "utilisation": psutil.virtual_memory().percent,
        "temperature": None,
        "power_consumption": None,
    })

    db.insert_hardware(_time, {
        "component": "disk_space",
        "hw_id": None,
        "utilisation": disk_space.percent,
        "temperature": None,
        "power_consumption": None,
    })

    '''
    db.insert_hardware(_time, {
        "component": "disk_usage",
        "hw_id": None,
        "utilisation": disk_space.read_count,
        "temperature": None,
        "power_consumption": None,
    })
    '''
    #    for item in network_usage:
    #        db.insert_hardware(_time, {
    #            "component": "network",
    #            "hw_id": none,
    #            "utilisation": network_usage[item].bytes_recv + network_usage[item].bytes_sent,
    #            "temperature": None,
    #            "power_consumption": None,
    #        })
    for item in network_usage:
        networksum = networksum + network_usage[item].bytes_recv + network_usage[item].bytes_sent

    db.insert_hardware(_time, {
        "component": "network",
        "hw_id": None,
        "utilisation": networksum,
        "temperature": None,
        "power_consumption": None,
    })
    #    db.insert_hardware(_time, {
    #        "component": "network",
    #        "hw_id": None,
    #        "utilisation": network_usage.bytes_recv + network_usage.bytes_sent,
    #        "temperature": None,
    #        "power_consumption": None,
    #    })

    db.insert_hardware(_time, {
        "component": "cpu",
        "hw_id": None,
        "utilisation": psutil.cpu_percent(),
        "temperature": get_CPUTemps(),
        #        "temperature": temperatures,
        "power_consumption": None,
    })

    for gpu in GPUtil.getGPUs():
        db.insert_hardware(_time, {
            "component": "gpu",
            "hw_id": gpu.id,
            "utilisation": gpu.load * 100,
            "temperature": gpu.temperature,
            "power_consumption": float(exec("gpu_power", args=(gpu.id))),
        })

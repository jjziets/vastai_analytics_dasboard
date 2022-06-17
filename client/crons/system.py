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
    temperatures = psutil.sensors_temperatures()
    
    #cputemp = open("/sys/class/thermal/thermal_zone0/temp",'r').readlines()
    #temperatures = float(cputemp[0])/1000
    networksum=0


    def get_average(items):
        items = [item.current for item in items]
        return sum(items) / len(items)

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
        "temperature": get_average(temperatures['coretemp']),
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

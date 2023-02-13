#metrics.py file to define endpoint /metrics
from web.metrics import bp
from prometheus_client import (Gauge,generate_latest,REGISTRY,)

import psutil
import socket

# Get the host name of the machine
host = socket.gethostname()

# Define metrics for memory and cpu
ram_metric = Gauge("memory_usage_bytes", "Memory usage in bytes.",
                   {'host': host})
cpu_metric = Gauge("cpu_usage_percent", "CPU usage percent.",
                   {'host': host})

@bp.route("/metrics", methods=["GET"])
def stats():

    # Add ram metrics
    ram = psutil.virtual_memory()
    ram_metric.labels('Ram used').set(ram.used)

    #Add cpu metrics
    cpu = psutil.cpu_percent()
    cpu_metric.labels('CPU percentage used').set(cpu)

    return generate_latest(REGISTRY), 200
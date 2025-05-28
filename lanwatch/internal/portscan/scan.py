import ssl
from contextlib import contextmanager
from typing import Optional, Dict, Any
import logging
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
import socket
from typing import Tuple
from dataclasses import dataclass

# Models
@dataclass
class Conf:
    InfluxAddr: str
    InfluxToken: str
    InfluxSkipTLS: bool
    InfluxOrg: str
    InfluxBucket: str

@dataclass
class Host:
    IP: str
    Iface: str
    Name: str
    Mac: str
    Known: int
    Now: int

# InfluxDB functions
def add(app_config: Conf, one_hist: Host) -> None:
    """Write data to InfluxDB2"""
    
    client = InfluxDBClient(
        url=app_config.InfluxAddr,
        token=app_config.InfluxToken,
        org=app_config.InfluxOrg,
        ssl=not app_config.InfluxSkipTLS,
        verify_ssl=not app_config.InfluxSkipTLS
    )
    
    try:
        # Check connection
        if not client.ping():
            logging.error("Can't connect to InfluxDB server")
            return

        # Escape special characters in strings
        name = one_hist.Name
        name = name.replace(" ", "\\ ")
        name = name.replace(",", "\\,")
        name = name.replace("=", "\\=")
        if not name:
            name = "unknown"

        # Create data point
        point = Point("WatchYourLAN") \
            .tag("IP", one_hist.IP) \
            .tag("iface", one_hist.Iface) \
            .tag("name", name) \
            .tag("mac", one_hist.Mac) \
            .tag("known", str(one_hist.Known)) \
            .field("state", one_hist.Now)

        # Write data
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=app_config.InfluxBucket, record=point)
        
    except Exception as e:
        logging.error(f"Error writing to InfluxDB: {e}")
    finally:
        client.close()

# Port scanning functions
def is_open(host: str, port: str, timeout: float = 3.0) -> bool:
    """Check if a TCP port is open"""
    try:
        target = f"{host}:{port}"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, int(port)))
            return result == 0
    except Exception:
        return False

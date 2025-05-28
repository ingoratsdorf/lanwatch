import os
import ssl
from typing import List, Optional
from dataclasses import dataclass
import logging
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

@dataclass
class Conf:
    host: str
    port: str
    theme: str
    color: str
    dir_path: str
    conf_path: str
    db_path: str
    node_path: str
    log_level: str
    ifaces: str
    arp_args: str
    arp_strs: List[str]
    timeout: int
    trim_hist: int
    hist_in_db: bool
    shout_url: str
    # PostgreSQL
    use_db: str
    pg_connect: str
    # InfluxDB
    influx_enable: bool
    influx_addr: str
    influx_token: str
    influx_org: str
    influx_bucket: str
    influx_skip_tls: bool
    # Prometheus
    prometheus_enable: bool

@dataclass
class Host:
    id: int
    name: str
    dns: str
    iface: str
    ip: str
    mac: str
    hw: str
    date: str
    known: int
    now: int

@dataclass
class Stat:
    total: int
    online: int
    offline: int
    known: int
    unknown: int

def add(app_config: Conf, one_hist: Host) -> None:
    """Write data to InfluxDB2"""
    
    tls_config = ssl.SSLContext()
    if app_config.influx_skip_tls:
        tls_config.verify_mode = ssl.CERT_NONE
    
    client = InfluxDBClient(
        url=app_config.influx_addr,
        token=app_config.influx_token,
        org=app_config.influx_org,
        ssl_context=tls_config
    )
    
    try:
        # Check connection
        if client.ping():
            write_api = client.write_api(write_options=SYNCHRONOUS)
            
            # Escape special characters in strings
            name = one_hist.name
            if not name:
                name = "unknown"
            else:
                name = name.replace(" ", "\\ ").replace(",", "\\,").replace("=", "\\=")
            
            point = Point("WatchYourLAN") \
                .tag("IP", one_hist.ip) \
                .tag("iface", one_hist.iface) \
                .tag("name", name) \
                .tag("mac", one_hist.mac) \
                .tag("known", str(one_hist.known)) \
                .field("state", one_hist.now)
            
            logging.debug("Writing to InfluxDB", extra={"line": str(point)})
            
            write_api.write(
                bucket=app_config.influx_bucket,
                org=app_config.influx_org,
                record=point
            )
        else:
            logging.error("Can't connect to InfluxDB server")
    except Exception as e:
        logging.error(f"Error writing to InfluxDB: {e}")
    finally:
        client.close()

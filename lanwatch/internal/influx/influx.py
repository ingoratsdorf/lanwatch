import contextlib
import ssl
from typing import Optional

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import logging

# Assuming these are the equivalent models in Python
class Conf:
    def __init__(self, influx_addr: str, influx_token: str, influx_org: str, 
                 influx_bucket: str, influx_skip_tls: bool):
        self.influx_addr = influx_addr
        self.influx_token = influx_token
        self.influx_org = influx_org
        self.influx_bucket = influx_bucket
        self.influx_skip_tls = influx_skip_tls

class Host:
    def __init__(self, ip: str, iface: str, name: str, mac: str, known: int, now: int):
        self.ip = ip
        self.iface = iface
        self.name = name
        self.mac = mac
        self.known = known
        self.now = now

def if_error(err: Optional[Exception]):
    if err is not None:
        logging.error(err)

def add(app_config: Conf, one_hist: Host):
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
            one_hist.name = one_hist.name.replace(" ", "\\ ").replace(",", "\\,").replace("=", "\\=")
            if not one_hist.name:
                one_hist.name = "unknown"

            point = Point("WatchYourLAN") \
                .tag("IP", one_hist.ip) \
                .tag("iface", one_hist.iface) \
                .tag("name", one_hist.name) \
                .tag("mac", one_hist.mac) \
                .tag("known", str(one_hist.known)) \
                .field("state", one_hist.now)

            logging.debug(f"Writing to InfluxDB: {point.to_line_protocol()}")
            
            try:
                write_api.write(bucket=app_config.influx_bucket, record=point)
            except Exception as e:
                if_error(e)
        else:
            logging.error("Can't connect to InfluxDB server")
    except Exception as e:
        if_error(e)
    finally:
        client.close()

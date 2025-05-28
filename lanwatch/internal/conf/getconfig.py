import yaml
import os
import logging

class Config:
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = "8840"
        self.theme = "sand"
        self.color = "dark"
        self.node_path = ""
        self.log_level = "info"
        self.arp_args = ""
        self.arp_strs = []
        self.ifaces = ""
        self.timeout = 120
        self.trim_hist = 48
        self.hist_in_db = False
        self.shout_url = ""
        self.use_db = "sqlite"
        self.pg_connect = ""
        self.influx_enable = False
        self.influx_skip_tls = False
        self.influx_addr = ""
        self.influx_token = ""
        self.influx_org = ""
        self.influx_bucket = ""
        self.prometheus_enable = False
        self.conf_path = ""

    @staticmethod
    def read_config(path):
        """Read YAML configuration file"""
        config = Config()
        config.conf_path = path

        if not os.path.exists(path):
            logging.error(f"Config file not found: {path}. Returning default configuration.")
            return config

        with open(path, "r") as file:
            data = yaml.safe_load(file)

        for key, value in data.items():
            if hasattr(config, key.lower()):
                setattr(config, key.lower(), value)

        return config

    def write_config(self):
        """Write configuration to a YAML file"""
        data = {attr.upper(): getattr(self, attr) for attr in vars(self)}

        with open(self.conf_path, "w") as file:
            yaml.safe_dump(data, file)

        logging.info(f"Configuration saved to {self.conf_path}")

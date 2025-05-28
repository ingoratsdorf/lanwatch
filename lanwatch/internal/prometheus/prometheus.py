# prometheus.py
from http import HTTPStatus
from typing import Callable

from prometheus_client import Gauge, generate_latest, REGISTRY
from prometheus_client.exposition import MetricsHandler
from flask import Response, request

class PrometheusMetrics:
    def __init__(self):
        self.up = Gauge(
            'watch_your_lan_up',
            'Whether the host is up (1 for yes, 0 for no)',
            ['ip', 'iface', 'name', 'mac', 'known']
        )

    def handler(self, app_config: dict) -> Callable:
        """Display Prometheus metrics"""
        def prometheus_handler():
            if not app_config.get('prometheus_enable', False):
                return Response(status=HTTPStatus.NOT_FOUND)
            return generate_latest(REGISTRY)
        return prometheus_handler

    def add(self, host: dict):
        """Add a Prometheus metric"""
        if not host.get('name'):
            host['name'] = 'unknown'
        
        self.up.labels(
            ip=host['ip'],
            iface=host['iface'],
            name=host['name'],
            mac=host['mac'],
            known=str(host.get('known', 0))
        ).set(float(host.get('now', 0)))


# Initialize the metrics instance
metrics = PrometheusMetrics()

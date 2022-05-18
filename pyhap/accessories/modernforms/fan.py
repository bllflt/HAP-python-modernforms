import logging

import requests

logger = logging.getLogger(__name__)


class ModernFormsFan:

    config_map = {
        'AccessoryInformation': {
            'Model': {
                'device_key': 'fanType'
            },
            'FirmwareRevision': {
                'device_key': 'mainMcuFirmwareVersion'
            },
            'Manufacturer': {
                'value': 'Modern Forms'
            },
            'Name': {
                'device_key': 'deviceName'
            },
            'SerialNumber': {
                'device_key': 'mac'
            },
        },
        'Fan': {
            'On': {
                'device_key': 'fanOn'
            },
            'RotationSpeed': {
                'device_key': 'fanSpeed',
                'properties': {"step": 17},
                'from_device': lambda value: round(16.66 * value),
                'to_device': lambda value: round(value/16.66)
            },
            'RotationDirection': {
                'device_key': 'fanDirection',
                'from_device':
                lambda value: {'reverse': 0,
                               'forward': 1}[value],
                'to_device':
                lambda value: {0: 'reverse',
                               1: 'forward'}[value]}
        },
        'Lightbulb': {
            'On': {
                'device_key': 'lightOn',
            },
            'Brightness': {
                'device_key': 'lightBrightness'
            }
        }
    }

    def device_config(self, srv, char):
        if 'device_key' in self.config_map[srv][char]:
            key = self.config_map[srv][char]['device_key']
            raw_value = self._device_config[key]
            if ('from_device' not in self.config_map[srv][char]):
                return raw_value
            else:
                return self.config_map[srv][char]['from_device'](raw_value)
        else:
            return self.config_map[srv][char]['value']

    def build_desired_config(self, srv, chars):
        desired_config = {}
        for char, value in chars.items():
            config_key = self.config_map[srv][char]['device_key']
            if ('to_device' in self.config_map[srv][char]):
                value = self.config_map[srv][char]['to_device'](value)
            desired_config[config_key] = value
        return desired_config

    def push_device_config(self, srv, chars):
        payload = self.build_desired_config(srv, chars)
        self.http_post(payload)

    def available(self) -> bool:
        return self._available

    def __init__(self, host, timeout=5):
        self._api_url = "http://{0}/mf".format(host)
        self._device_config = {}
        self._available = True
        self._timeout = timeout

    def http_post(self, payload):
        response = {}
        try:
            api = requests.post(
                self._api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=self._timeout
            )
        except requests.exceptions.RequestException as e:
            logger.warn(e, exec_info=True)
            self._available = False
        else:
            self._available = True
            response = api.json()
        finally:
            return response

    def fetch_device_config(self, key):
        self._device_config.update(self.http_post({key: '1'}))

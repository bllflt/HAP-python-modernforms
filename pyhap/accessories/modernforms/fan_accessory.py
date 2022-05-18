from pyhap.accessories.modernforms.fan import ModernFormsFan
from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_FAN


class ModernFormsFanAccessory(Accessory):

    category = CATEGORY_FAN

    def __init__(self, *args, fan: ModernFormsFan, **kwargs):
        super().__init__(*args, **kwargs)

        self._fan = fan

        self.set_info_service(
            firmware_revision=self._fan.device_config(
                'AccessoryInformation', 'FirmwareRevision'),
            manufacturer=self._fan.device_config(
                'AccessoryInformation', 'Manufacturer'),
            model=self._fan.device_config('AccessoryInformation', 'Model'),
            serial_number=self._fan.device_config(
                'AccessoryInformation', 'SerialNumber'),
        )

        self.my_characteristics = []
        for service_name in (self._fan.config_map.keys()):
            if service_name == 'AccessoryInformation':
                continue
            char_names = list(self._fan.config_map[service_name].keys())
            srv = self.add_preload_service(service_name, chars=char_names)
            for char_name in char_names:
                cfg_m_entry = self._fan.config_map[service_name][char_name]
                char = srv.configure_char(char_name)
                if ('properties' in cfg_m_entry):
                    char.override_properties(
                        properties=cfg_m_entry['properties'])
                self.my_characteristics.append((service_name, char_name, char))

            srv.setter_callback = self.make_service_setter_callback(
                service_name)

    def make_service_setter_callback(self, service_name):
        def cb(chars):
            self._fan.push_device_config(service_name, chars)
        return cb

    def update_values(self):
        for char_t in self.my_characteristics:
            value = self._fan.device_config(char_t[0], char_t[1])
            char_t[2].set_value(value)

    def available(self):
        return self._fan.available

    @Accessory.run_at_interval(10)
    async def run(self):
        self._fan.fetch_device_config('queryDynamicShadowData')
        self.update_values

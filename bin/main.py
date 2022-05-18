import os
import signal

from dotenv import load_dotenv
from pyhap.accessories.modernforms.fan import ModernFormsFan
from pyhap.accessories.modernforms.fan_accessory import ModernFormsFanAccessory
from pyhap.accessory_driver import AccessoryDriver

load_dotenv()
fan_ip = os.environ.get('MODERN_FORM_FAN_IP')

driver = AccessoryDriver(port=51826)
fan = ModernFormsFan(fan_ip)
fan.fetch_device_config('queryStaticShadowData')
name = fan.device_config('AccessoryInformation', 'Name')
driver.add_accessory(accessory=ModernFormsFanAccessory(driver, name, fan=fan))

signal.signal(signal.SIGTERM, driver.signal_handler)

driver.start()

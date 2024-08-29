import random
import asyncio
from bluez_peripheral.advert import struct
from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags
from bluez_peripheral.gatt.descriptor import descriptor, DescriptorFlags as DescFlags

SERVICE_MEASUREMENT = '00cfb9c8-4851-4807-b88d-9d963460a815'

class MeasurementService(Service):
    voltage = 0.0
    to_update_voltage = False

    def _gen_voltage(self):
        if random.random() > .75:
            self.voltage = round(random.uniform(5, 7), 1)
            print(f"New voltage: {self.voltage}")

    def __init__(self):
        super().__init__(SERVICE_MEASUREMENT, True)
        self._gen_voltage()
        self.to_update_voltage = True
        asyncio.run_coroutine_threadsafe(self.update_voltage(),
                                         asyncio.get_event_loop())

    @characteristic('2B18', CharFlags.READ | CharFlags.NOTIFY)
    def voltage_characteristic(self, options):
        return struct.pack('f', self.voltage)

    async def update_voltage(self):
        while self.to_update_voltage:
            self._gen_voltage()
            self.voltage_characteristic.changed(struct.pack('f', self.voltage))
            await asyncio.sleep(1)

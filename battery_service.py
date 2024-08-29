import asyncio
import psutil
from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags
from bluez_peripheral.gatt.descriptor import descriptor, DescriptorFlags as DescFlags

SERVICE_BATTERY = '180F'

class BatteryService(Service):
    def __init__(self):
        super().__init__(SERVICE_BATTERY, True)
        self.to_update_energy_level = True
        asyncio.run_coroutine_threadsafe(self.update_energy_level(),
                                         asyncio.get_event_loop())

    @characteristic('2A19', CharFlags.READ | CharFlags.NOTIFY)
    def energy_characteristic(self, options):
        batt_level = int(psutil.sensors_battery().percent)
        return batt_level.to_bytes()

    async def update_energy_level(self):
        while self.to_update_energy_level:
            batt_level = int(psutil.sensors_battery().percent)
            self.energy_characteristic.changed(batt_level.to_bytes())
            await asyncio.sleep(30)

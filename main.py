import asyncio
from bluez_peripheral.util import *
from bluez_peripheral.agent import NoIoAgent
from bluez_peripheral.advert import Advertisement, AdvertisingIncludes

from battery_service import SERVICE_BATTERY, BatteryService
from measurement_service import SERVICE_MEASUREMENT, MeasurementService

async def main():
    bus = await get_message_bus()
    battery_service = BatteryService()
    await battery_service.register(bus, '/space/diomentia/battery_service')
    measurement_service = MeasurementService()
    await measurement_service.register(bus, '/space/diomentia/measurement_service')
    agent = NoIoAgent()
    await agent.register(bus)
    adapter = await Adapter.get_first(bus)
    advertisement = Advertisement(
            "PTM MIK",
            [SERVICE_BATTERY, SERVICE_MEASUREMENT],
            0x0484,
            3600)
    await advertisement.register(bus, adapter)
    print('Advertisement online!')
    await bus.wait_for_disconnect()

if __name__ == '__main__':
    asyncio.run(main())

import asyncio
from bluez_peripheral.util import *
from bluez_peripheral.agent import NoIoAgent
from bluez_peripheral.advert import Advertisement, AdvertisingIncludes

from battery_service import BatteryService

async def main():
    bus = await get_message_bus()
    await BatteryService().register(bus)
    agent = NoIoAgent()
    await agent.register(bus)
    adapter = await Adapter.get_first(bus)
    advertisement = Advertisement("PTM MIK", ['180F'], 0x0441, 60)
    await advertisement.register(bus, adapter)
    await bus.wait_for_disconnect()

if __name__ == '__main__':
    asyncio.run(main())

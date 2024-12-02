from bleak import BleakClient
import asyncio

async def scan_device(mac):
    async with BleakClient(mac) as client:
        print("Connected:", client.is_connected)
        for service in client.services:
            print(f"Service: {service.uuid}")
            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid} - Properties: {char.properties}")

asyncio.run(scan_device("30:58:95:04:56:f9"))

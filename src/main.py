import asyncio

async def _main():

    print("Hello World!")

    import modules.ota_manager as _ota

    ota_man = _ota.OTAManager(in_simulator=False)

if __name__ == "__main__":
    # Start all the tasks and main event loop.
    asyncio.create_task(_main())
    asyncio.get_event_loop().run_forever()

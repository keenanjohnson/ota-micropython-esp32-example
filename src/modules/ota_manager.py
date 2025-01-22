import asyncio
import logging

from micropython import const

from modules.aiohttp import ClientSession

from json import loads

import __version__

MAIN_UPDATE_URL = const("https://github.com/keenanjohnson/ota-micropython-esp32-example/release/ota.json")

try:
    # The OTA manager requires the esp32 library, which is only available
    # on the ESP32 platform.
    import modules.ota.status
    import modules.ota.rollback
    import modules.ota.update
except ImportError:
    pass

class OTAManager:
    def __init__(self, in_simulator=False):
        self.in_simulator = in_simulator
        self._logger = logging.getLogger(__name__)

        self._fw_version = __version__.version

        self._logger.info("Starting OTA Manager")

        # Check whether the beta flag in the version file is set to True
        beta = __version__.beta
        

        self.update_url = MAIN_UPDATE_URL

        # Print a message indicating whether this is a beta unit or not
        if beta:
            self._logger.info("This is a beta unit")
        else:
            self._logger.info("This is a production unit")
        self._logger.info("Update URL: %s", self.update_url)

        if not self.in_simulator:
            # Assuming we previously booted, if we have arrived here, the update
            # was successful, so mark it as such.
            # Don't run this in the simulator, as it will fail.
            self.declare_boot_successful()

        # Start the update loop
        self.update_loop_task = asyncio.create_task(self.update_loop())

    async def update_loop(self):
        """
        The main loop that checks for a new update and then performs the update.
        """

        await asyncio.sleep(10)

        new_update = False
        
        while True:
            try:
                new_update = await self.check_for_updates()
            except Exception as e:
                self._logger.error("Error checking for updates: %s", e)

            if new_update:
                self._logger.info("New update available")
                self.print_ota_status()
                self.do_update_from_json_at_url(self.update_url)

                self._logger.info("Update complete")
                self.print_ota_status()
            else:
                await asyncio.sleep(30)


    async def check_for_updates(self):
        self._logger.info("Checking for updates")

        server_version = await self.get_version_from_url()

        self._logger.info("OTA: Current FW Version: %s, Server FW Version: %s",  self._fw_version, server_version)

        # Compare our version to the server version. If they are different, we
        # have an update.
        if server_version != self._fw_version:
            self._logger.info("New update available")
            return True
        else:
            self._logger.info("No new update available")
            return False

    async def fetch_data_from_url(self, client, url):
        """
        Get the data from the URL. This should be a text json file.
        """
        async with client.get(url) as resp:
            assert resp.status == 200
            return await resp.text()

    async def get_version_from_url(self):
        """
        Get the version from the URL. This should be a text json file.
        """

        async with ClientSession() as client:
            version_file = await self.fetch_data_from_url(client, self.update_url)

            # Convert the json to a dictionary
            version_dict = loads(version_file)

            version = version_dict["version"]

            return version

    def do_update_from_json_at_url(self, url):
        """
        This function downloads the firmware json from the URL,
        downloads the firmware binary from the URL in the json,
        and runs the OTA update process, including rebooting the device.
        """

        # Don't run in sim
        if self.in_simulator:
            return

        try:
            modules.ota.update.from_json(url=url, verbose=True, reboot=True)
        except Exception as e:
            self._logger.error("Error updating firmware: %s", e)

    def print_ota_status(self):
        """
        This function prints the status of the OTA partitions.
        """

        # Don't run in sim
        if self.in_simulator:
            return

        modules.ota.status.status()

    def declare_boot_successful(self):
        """
        This function should be called after a successful OTA.
        It marks the current firmware as the one to boot from. Otherwise, on
        the next boot, the previous firmware from the other parition will be
        restored.
        """

        # Don't run in sim
        if self.in_simulator:
            return

        # Somewhat confusingly the method to mark the current firmware as 
        # valid is called cancel.
        modules.ota.rollback.cancel()

        self._logger.info("OTA Boot successful. Marking partition as valid.")

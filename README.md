# ota-micropython-esp32-example
This repo is an example of how to implement the basics of OTA in micropython on an esp32s3 over the wifi radio.

### What's Unique
There are several other examples of how to implement OTA in a variety of ways, but this example is unique in a few ways that might be interesting to you:

* It shows how to precompile the python files into bytecode, which has the advantage of allowing us to transmit a single .bin file to the device to do an update, rather than each individual .py files
    * See more about the freezing / precompilation process [here.](https://docs.micropython.org/en/latest/reference/manifest.html#summary)
* The OTA Management class is designed to work within the async framework.
* It utilizes the excellent library from https://github.com/glenn20/micropython-esp32-ota as a starting place
* It demonstrates how to build the .bin file via github actions
* It demonstrates how to host the compiled binary images on github. 

### How It Works
The basic idea is that the device will check a github repository for a new version of the firmware. If a new version is found, it will download the new firmware and write it to the flash memory.

The "current" version of the firmware is stored in the ota.json file.

The OTA Manager class checks that file on a period and will initiate the download and update process if a new version is found.

### Hardware

This example is specifically targetting the esp32s3 with 4MB Flash 2MB PSRAM.

Specifically I've used this board in the feather form factor from Adafruit to much success in several projects.

https://www.adafruit.com/product/5477

![image](https://github.com/user-attachments/assets/7f419e60-7f1b-4412-897e-798cfacb56c2)

### What this Example Does NOT Address

* This example doesn't really take into account any security aspects. If security is important for your application, you will need to add additional security steps to this example or consider a different approach.


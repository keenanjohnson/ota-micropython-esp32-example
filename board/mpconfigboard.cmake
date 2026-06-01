set(IDF_TARGET esp32s3)

# Note: native USB-CDC is now enabled automatically on the S3
# (MICROPY_HW_ENABLE_USBDEV defaults to SOC_USB_OTG_SUPPORTED), so the old
# boards/sdkconfig.usb fragment no longer exists and is not needed here.
set(SDKCONFIG_DEFAULTS
    boards/sdkconfig.base
    boards/sdkconfig.240mhz
    boards/sdkconfig.spiram_sx
    boards/ota-example/sdkconfig.board
)

MP_DIR := ${CURDIR}/vendor/micropython
PORT_DIR := ${MP_DIR}/ports/esp32
BOARD := ota-example
BUILD_DIR := ${PORT_DIR}/build-${BOARD}

DEVICE := /dev/tty.usbmodem2101

.PHONY: build
build: ${MP_DIR}/mpy-cross/build/mpy-cross
	rm -f ${BUILD_DIR}/frozen_content.c
	ln -sfn ${CURDIR}/board ${PORT_DIR}/boards/${BOARD}
	make -C ${PORT_DIR} BOARD=${BOARD} FROZEN_MANIFEST=${CURDIR}/manifest.py
	mkdir -p ./firmware
	cp ${BUILD_DIR}/bootloader/bootloader.bin ${BUILD_DIR}/partition_table/partition-table.bin ${BUILD_DIR}/ota_data_initial.bin ${BUILD_DIR}/micropython.bin ./firmware

# Workaround: mpy-cross fails to build with FROZEN_MANIFEST set
# Remove when that is fixed in MicroPython
# https://github.com/micropython/micropython/issues/13385
${MP_DIR}/mpy-cross/build/mpy-cross:
	make -C ${MP_DIR}/mpy-cross

${UNIX_DIR}/build-standard/micropython: ${MP_DIR}/mpy-cross/build/mpy-cross
	make -C ${MP_DIR}/ports/unix -j FROZEN_MANIFEST=${CURDIR}/manifest-unix.py

.PHONY: flash
flash: build
	esptool.py -p ${DEVICE} -b 460800 --before default_reset --after no_reset \
		--chip esp32s3 \
		write_flash --flash_mode dio --flash_size detect --flash_freq 80m \
		0x0 firmware/bootloader.bin \
		0x8000 firmware/partition-table.bin \
		0xd000 firmware/ota_data_initial.bin \
		0x10000 firmware/micropython.bin

.PHONY: clean
clean:
	rm -rf ${BUILD_DIR} ${UNIX_DIR}/build-standard

.PHONY: erase
erase:
	esptool.py --chip esp32s3 --port ${DEVICE} erase_flash


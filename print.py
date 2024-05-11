import usb.backend.libusb1

# Manually specify the path to the libusb library
backend = usb.backend.libusb1.get_backend(find_library=lambda x: "/opt/homebrew/lib/libusb-1.0.dylib")
if backend is None:
    print("Backend not loaded.")
else:
    from escpos.printer import Usb
    # set the printer profile to You can select this profile in python-escpos with this identifier: TM-T20II. (Set parameter to profile=’TM-T20II’.)

    

    # Initialize printer with the loaded backend
    # printer = Usb(0x04b8, 0x0202, 0, 0x81, 0x03, backend=backend)
    printer = Usb(0x04b8, 0x0202, profile='TM-T20II-42col')
    #printer.text("Hello World\n")
    printer.image("receipt_1.png")
    printer.cut()

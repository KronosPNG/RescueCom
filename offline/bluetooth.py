import asyncio
import signal

import dbus
import dbus.mainloop.glib
import dbus.service
from gi.repository import GLib

BLUEZ_SERVICE_NAME = "org.bluez"
LE_ADVERTISING_MANAGER_IFACE = "org.bluez.LEAdvertisingManager1"
DBUS_OM_IFACE = "org.freedesktop.DBus.ObjectManager"
DBUS_PROP_IFACE = "org.freedesktop.DBus.Properties"
LE_ADVERTISEMENT_IFACE = "org.bluez.LEAdvertisement1"


class Broadcaster:
    def __init__(self, local_name: str) -> None:
        self.local_name = local_name
        self.mainloop = None
        self.advertisement = None

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()

        # Ensure Power is ON
        adapter_props = dbus.Interface(
            self.bus.get_object(BLUEZ_SERVICE_NAME, "/org/bluez/hci0"), DBUS_PROP_IFACE
        )
        adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

        self.ad_manager = dbus.Interface(
            self.bus.get_object(BLUEZ_SERVICE_NAME, "/org/bluez/hci0"),
            LE_ADVERTISING_MANAGER_IFACE,
        )

    async def broadcast(self, payload: list[int] | bytes):
        self.advertisement = Advertisement(self.bus, 0, self.local_name)

        self.advertisement.add_data(0xFFFF, payload)

        self.mainloop = GLib.MainLoop()

        def signal_handler(sig, frame):
            if self.mainloop:
                self.mainloop.quit()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        self.ad_manager.RegisterAdvertisement(
            self.advertisement.get_path(),
            {},
            reply_handler=lambda: print("Broadcasted successfully!"),
            error_handler=lambda x: print(f"Error: {x}"),
        )

        try:
            self.mainloop.run()
        finally:
            try:
                self.ad_manager.UnregisterAdvertisement(self.advertisement.get_path())
            except Exception as e:
                print(f"Error while closing: {e}")

    # TODO: add a method to gracefully stop the broadcasting


class Advertisement(dbus.service.Object):
    def __init__(self, bus: dbus.SystemBus, index: int, local_name: str) -> None:
        self.path = "/org/bluez/example/advertisement" + str(index)
        self.bus = bus
        self.ad_type = "peripheral"
        self.local_name = local_name
        # signature='qv' means: Key is uint16, Value is VARIANT
        self.manufacturer_data = dbus.Dictionary({}, signature="qv")
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        properties = dict()
        properties["Type"] = self.ad_type
        properties["LocalName"] = dbus.String(self.local_name)

        # We pass the dictionary directly.
        # Since it was created with signature='qv', it is already compliant.
        properties["ManufacturerData"] = self.manufacturer_data

        # Disable TX Power
        properties["Includes"] = dbus.Array([], signature="s")
        return properties

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_data(self, key, data):
        # We just create the Array. We let the Dictionary's signature ('qv')
        # force the library to wrap this in a Variant automatically.
        val = dbus.Array(data, signature="y")
        self.manufacturer_data[key] = val

    @dbus.service.method(DBUS_PROP_IFACE, in_signature="s", out_signature="a{sv}")
    def GetAll(self, interface):
        return self.get_properties()

    @dbus.service.method(LE_ADVERTISEMENT_IFACE, in_signature="", out_signature="")
    def Release(self):
        print("Advertisement released")

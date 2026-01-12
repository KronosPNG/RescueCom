import asyncio
import threading
import time
from typing import Optional

import dbus
import dbus.mainloop.glib
import dbus.service
from gi.repository import GLib

# Setup - Common
BLUEZ_SERVICE_NAME = "org.bluez"
DBUS_OM_IFACE = "org.freedesktop.DBus.ObjectManager"
DBUS_PROP_IFACE = "org.freedesktop.DBus.Properties"

# Setup - Broadcaster
LE_ADVERTISING_MANAGER_IFACE = "org.bluez.LEAdvertisingManager1"
LE_ADVERTISEMENT_IFACE = "org.bluez.LEAdvertisement1"

# Setup - Listener
DEVICE_IFACE = "org.bluez.Device1"
ADAPTER_IFACE = "org.bluez.Adapter1"


dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)


class Broadcaster:
    def __init__(self, local_name: str) -> None:
        self.local_name = local_name
        self.mainloop = None
        self.bus = dbus.SystemBus()
        self.advertisement = Advertisement(self.bus, 0, self.local_name)
        self.is_broadcasting = False

        # Ensure Power is ON
        adapter_props = dbus.Interface(
            self.bus.get_object(BLUEZ_SERVICE_NAME, "/org/bluez/hci0"), DBUS_PROP_IFACE
        )
        adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

        self.ad_manager = dbus.Interface(
            self.bus.get_object(BLUEZ_SERVICE_NAME, "/org/bluez/hci0"),
            LE_ADVERTISING_MANAGER_IFACE,
        )

    def broadcast(self, payload: list[int] | bytes) -> None:
        """
        Starts broadcasting a payload over Bluetooth LE.

        Registers a Bluetooth LE advertisement containing the given payload
        as manufacturer-specific data. If broadcasting is already active,
        the method returns without doing anything.

        Args:
            payload (list[int] | bytes): The data to broadcast as manufacturer data.
        """

        if self.is_broadcasting:
            return

        self.advertisement.manufacturer_data.clear()

        self.advertisement.add_data(0xFFFF, payload)

        self.ad_manager.RegisterAdvertisement(
            self.advertisement.get_path(),
            {},
            reply_handler=self._on_success,
            error_handler=lambda x: print(f"Broadcaster Error: {x}"),
        )

        self.mainloop = GLib.MainLoop()
        self.mainloop_thread = threading.Thread(target=self._run_mainloop, daemon=True)
        self.mainloop_thread.start()

    def _run_mainloop(self):
        try:
            if self.mainloop is not None:
                self.mainloop.run()
        except Exception as e:
            print(f"MainLoop error: {e}")

    def _on_success(self):
        print("Broadcasting started successfully!")
        self.is_broadcasting = True

    def stop(self) -> None:
        """
        Stops the Bluetooth LE broadcast.

        Unregisters the active advertisement, stops broadcasting,
        and removes the advertisement object from DBus.
        """

        if self.is_broadcasting:
            try:
                self.ad_manager.UnregisterAdvertisement(self.advertisement.get_path())
                print("Broadcasting stopped.")
                self.is_broadcasting = False
            except Exception as e:
                print(f"Error stopping broadcast: {e}")

            if self.advertisement:
                try:
                    self.advertisement.remove_from_connection()
                except Exception as e:
                    print(f"Error removing advertisement from DBus: {e}")

                self.advertisement = None

    def update_payload(self, payload: list[int] | bytes) -> None:
        """
        Updates the broadcast payload.

        Stops the current broadcast if active and restarts it with
        the new payload.

        Args:
            payload (list[int] | bytes): The new data to broadcast.
        """

        if self.is_broadcasting:
            self.ad_manager.UnregisterAdvertisement(self.advertisement.get_path())
            self.is_broadcasting = False
            time.sleep(0.1)

        self.broadcast(payload)


# TODO: convert to Singleton (?)
class Listener:
    def __init__(
        self,
        target_name: str,
        max_queue_size: int = 100,
    ) -> None:
        self.target_name = target_name
        self.discovery_started = False
        self.mainloop_thread = None
        self.mainloop = None
        self.results: list = []
        self.payload_queue: asyncio.Queue[bytes] = asyncio.Queue(maxsize=max_queue_size)
        self.__last_payload: bytes = bytes()

        self.bus = dbus.SystemBus()

        # Get adapter
        self.adapter_path = "/org/bluez/hci0"

        try:
            adapter_obj = self.bus.get_object(BLUEZ_SERVICE_NAME, self.adapter_path)
            adapter_props = dbus.Interface(adapter_obj, DBUS_PROP_IFACE)
            self.adapter = dbus.Interface(adapter_obj, ADAPTER_IFACE)

            # Ensure Power is ON
            adapter_props.Set(ADAPTER_IFACE, "Powered", dbus.Boolean(True))

            # Set discovery filter
            self.adapter.SetDiscoveryFilter(
                {
                    "Transport": dbus.String("le"),  # Only LE devices
                    "DuplicateData": dbus.Boolean(True),
                }
            )
        except dbus.exceptions.DBusException as e:
            print(f"Error setting up adapter: {e}")
            raise e

    def listen(self) -> None:
        """
        Starts listening for Bluetooth LE advertisements.

        Scans for already known devices, registers DBus signal handlers,
        starts device discovery, and runs the GLib main loop in a
        background thread.
        """

        # Get existing devices first
        print("Checking existing devices...")
        try:
            self._scan_existing_devices()
        except Exception as e:
            print(f"Error while scanning for existing devices: {e}")
            raise e

        # Listen for signals
        self.bus.add_signal_receiver(
            self._interfaces_added,
            dbus_interface=DBUS_OM_IFACE,
            signal_name="InterfacesAdded",
        )

        # Hook into DBus signals to catch new devices (InterfacesAdded)
        # and updates to existing devices (PropertiesChanged)
        self.bus.add_signal_receiver(
            self._interfaces_added,
            dbus_interface=DBUS_OM_IFACE,
            signal_name="InterfacesAdded",
        )
        self.bus.add_signal_receiver(
            self._properties_changed,
            dbus_interface=DBUS_PROP_IFACE,
            signal_name="PropertiesChanged",
            arg0=DEVICE_IFACE,
            path_keyword="path",
        )

        try:
            self.discovery_started = True
            self.adapter.StartDiscovery()
        except dbus.exceptions.DBusException as e:
            print(f"Discovery error: {e}")
            raise e

        self.mainloop = GLib.MainLoop()
        self.mainloop_thread = threading.Thread(target=self._run_mainloop, daemon=True)
        self.mainloop_thread.start()

    def _run_mainloop(self):
        try:
            if self.mainloop is not None:
                self.mainloop.run()
        except Exception as e:
            print(f"MainLoop error: {e}")

    def stop(self) -> None:
        """
        Gracefully stops Bluetooth discovery.

        Stops device discovery if it is currently active.
        """
        if self.discovery_started:
            try:
                self.adapter.StopDiscovery()
            except Exception:
                pass  # Discovery might already be stopped

    def get_payload_nowait(self) -> Optional[bytes]:
        """
        Retrieves the next received payload without blocking.

        Returns the next payload from the internal queue if available.

        Returns:
            Optional[bytes]: The next payload, or None if the queue is empty.
        """

        try:
            return self.payload_queue.get_nowait()
        except asyncio.QueueEmpty:
            return None

    @property
    def has_payloads(self) -> bool:
        return not self.payload_queue.empty()

    @property
    def queue_size(self) -> int:
        return self.payload_queue.qsize()

    def _scan_existing_devices(self):
        """Scan devices that are already known to BlueZ"""
        try:
            om = dbus.Interface(
                self.bus.get_object(BLUEZ_SERVICE_NAME, "/"), DBUS_OM_IFACE
            )
            objects = om.GetManagedObjects()

            for path, interfaces in objects.items():
                if DEVICE_IFACE in interfaces:
                    properties = interfaces[DEVICE_IFACE]
                    self._process_device(path, properties)
        except Exception as e:
            print(f"Error scanning existing devices: {e}")
            raise e

    def _interfaces_added(self, path, interfaces):
        """Called when a new device is discovered"""
        if DEVICE_IFACE not in interfaces:
            return

        properties = interfaces[DEVICE_IFACE]
        try:
            self._process_device(path, properties)
        except Exception as e:
            print(f"Error processing the device {path}: {e}")

    def _properties_changed(self, interface, changed, invalidated, path):
        """Called when device properties change"""
        try:
            self._process_device(path, changed)
        except Exception as e:
            print(f"Error processing the device {path}: {e}")

    def _process_device(self, path, properties):
        """Process device data"""
        try:
            # Get device name
            name = None
            if "Name" in properties:
                name = str(properties["Name"])
            elif "Alias" in properties:
                name = str(properties["Alias"])

            # Check if this is our target device
            if name == self.target_name:
                # Extract manufacturer data
                if "ManufacturerData" in properties:
                    mfg_data = properties["ManufacturerData"]

                    for _, data in mfg_data.items():
                        # Convert dbus.Array to bytes
                        payload = bytes(data)
                        if payload != self.__last_payload:
                            self.__last_payload = payload

                            try:
                                self.payload_queue.put_nowait(payload)
                            except asyncio.QueueFull:
                                print("Warning: Queue is full, dropping oldest payload")
                                try:
                                    self.payload_queue.get_nowait()
                                    self.payload_queue.put_nowait(payload)
                                except Exception:
                                    pass

                    try:
                        self.adapter.RemoveDevice(path)
                    except Exception:
                        pass
                else:
                    print("No ManufacturerData found!")
        except Exception as e:
            print(f"Error processing device {path}: {e}")
            raise e


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

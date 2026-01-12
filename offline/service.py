import threading

from bluetooth import Broadcaster, Listener
from queues import ble_rx_queue, ble_tx_queue
from worker import ble_worker


class BLEService:
    def __init__(self, local_name: str, target_name: str):
        self.broadcaster = Broadcaster(local_name=local_name)
        self.listener = Listener(target_name=target_name)

        self._stop_event: threading.Event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        """
        Starts the BLE service.

        Launches a background thread that manages BLE broadcasting and listening.
        If the service is already running, the method returns without action.
        """

        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()

        self._thread = threading.Thread(
            target=ble_worker,
            args=(self.broadcaster, self.listener, self._stop_event),
            daemon=True,
        )
        self._thread.start()

    def stop(self, timeout: float = 2.0):
        """
        Stops the BLE service.

        Signals the background worker thread to stop and waits for it to terminate.

        Args:
            timeout (float, optional): Maximum time in seconds to wait for the
                worker thread to stop. Defaults to 2.0 seconds.
        """
        self._stop_event.set()

        if self._thread:
            self._thread.join(timeout=timeout)

    # Flask -> BLE
    def send_payload(self, payload: bytes) -> bool:
        """
        Queues a payload for Bluetooth LE transmission.

        Adds the given payload to the BLE transmission queue without blocking.

        Args:
            payload (bytes): The payload to send over Bluetooth LE.

        Returns:
            bool: True if the payload was successfully queued, False otherwise.
        """

        try:
            ble_tx_queue.put_nowait(payload)
            return True
        except Exception:
            return False

    # Db <- BLE
    def receive_payload_nowait(self) -> bytes | None:
        """
        Retrieves a received BLE payload without blocking.

        Returns the next available payload from the BLE reception queue, if any.

        Returns:
            bytes | None: The received payload, or None if no payload is available.
        """

        if ble_rx_queue.empty():
            return None
        return ble_rx_queue.get()

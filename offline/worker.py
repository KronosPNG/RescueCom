import queue
import threading
import time

from bluetooth import Broadcaster, Listener
from queues import ble_rx_queue, ble_tx_queue


def ble_worker(
    broadcaster: Broadcaster,
    listener: Listener,
    stop_event: threading.Event,
):
    """
    Background worker that manages BLE transmission and reception.

    This function runs in a dedicated thread, coordinating the BLE broadcaster
    and listener. It continuously:
        - Retrieves received BLE payloads from the listener and queues them
          for processing (BLE -> application).
        - Fetches outgoing payloads from the application queue and updates the
          broadcaster (application -> BLE).

    The loop runs until the provided `stop_event` is set, at which point the
    listener and broadcaster are stopped gracefully.

    Args:
        broadcaster (Broadcaster): The BLE broadcaster used for sending payloads.
        listener (Listener): The BLE listener used for receiving payloads.
        stop_event (threading.Event): Event used to signal the worker to stop.
    """

    listener.listen()

    try:
        while not stop_event.is_set():
            # RX BLE -> queue
            while listener.has_payloads:
                payload = listener.get_payload_nowait()
                if payload:
                    try:
                        ble_rx_queue.put_nowait(payload)
                    except queue.Full:
                        listener.get_payload_nowait()
                        ble_rx_queue.put_nowait(payload)

            # TX BLE <- Flask
            try:
                payload = ble_tx_queue.get(timeout=0.1)
                broadcaster.update_payload(payload)
            except queue.Empty:
                pass

            time.sleep(0.01)
    finally:
        listener.stop()
        broadcaster.stop()

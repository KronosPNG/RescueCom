from queue import Queue

ble_tx_queue: Queue[bytes] = Queue(maxsize=100)
ble_rx_queue: Queue[bytes] = Queue(maxsize=100)

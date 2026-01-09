import heapq

from typing import Self
from enum import Enum
from common.models.emergency import Emergency
from common.models.enc_emergency import EncryptedEmergency


class SeverityType(Enum):
    LOW = 0  # Severity score range: 0 <= x < 35
    MEDIUM = 1  # Severity score range: 35 <= x < 65
    HIGH = 2  # Severity score range: x >= 65


class EmergencyQueue:
    __instance = None

    min_medium_sev_score = 35
    min_high_sev_score = 65
    queue: list[list[tuple[int, float, Emergency | EncryptedEmergency]],] = [
        [],
        [],
        [],
    ]

    def __init__(self) -> None:
        if not EmergencyQueue.__instance:
            raise TypeError(
                "EmergencyQueue singleton must be created using EmergencyQueue.get_instance"
            )

        heapq.heapify_max(self.queue[SeverityType.LOW.value])  # Low severity
        heapq.heapify_max(self.queue[SeverityType.MEDIUM.value])  # Medium severity
        heapq.heapify_max(self.queue[SeverityType.HIGH.value])  # High severity

        self.low_queue = self.queue[SeverityType.LOW.value]
        self.medium_queue = self.queue[SeverityType.MEDIUM.value]
        self.high_queue = self.queue[SeverityType.HIGH.value]

    @classmethod
    def get_instance(cls: type[Self]) -> Self:
        """
        Returns the singleton instance of EmergencyQueue.

        Returns:
            EmergencyQueue: The singleton instance of the emergency queue.
        """

        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def push_emergency(self, emergency: Emergency | EncryptedEmergency):
        """
        Adds an emergency to the appropriate priority queue.

        This method inserts the given emergency into one of the internal
        priority queues based on its severity level. Emergencies are ordered
        primarily by severity and secondarily by creation time, ensuring that
        higher-severity and older emergencies are processed first.

        Args:
            emergency (Emergency | EncryptedEmergency): The emergency instance
                to be added to the queue.
        """

        severity = emergency.severity
        created_at = -emergency.created_at.timestamp()

        # TODO: Establish the maximum possible score
        if (severity >= 0) and (severity < self.min_medium_sev_score):
            heapq.heappush_max(
                self.low_queue,
                (severity, created_at, (emergency)),
            )
        elif (severity >= self.min_medium_sev_score) and (
            severity < self.min_high_sev_score
        ):
            heapq.heappush_max(
                self.medium_queue,
                (severity, created_at, emergency),
            )
        else:
            heapq.heappush_max(
                self.high_queue,
                (severity, created_at, emergency),
            )

    def pop_emergency(
        self, severity_type: SeverityType
    ) -> Emergency | EncryptedEmergency:
        """
        Removes and returns the highest-priority emergency from a queue.

        This method retrieves and removes the emergency with the highest
        priority from the queue corresponding to the specified severity type.

        Args:
            severity_type (SeverityType): The severity category from which to
                pop the emergency (LOW, MEDIUM, or HIGH).

        Returns:
            Emergency | EncryptedEmergency: The emergency instance with the
            highest priority in the selected queue.

        Raises:
            IndexError: If the selected queue is empty.
        """

        match severity_type:
            case SeverityType.LOW:
                return heapq.heappop_max(self.low_queue)[2]
            case SeverityType.MEDIUM:
                return heapq.heappop_max(self.medium_queue)[2]
            case SeverityType.HIGH:
                return heapq.heappop_max(self.high_queue)[2]

    def update_emergency(
        self, old_emergency_severity: int, emergency: Emergency | EncryptedEmergency
    ) -> None:
        """
        Updates an existing emergency in the priority queue.

        This method removes a previously queued emergency based on its old
        severity level and re-inserts the updated emergency into the
        appropriate priority queue. This allows the emergency to be
        re-prioritized if its severity or other relevant attributes have
        changed.

        A linear search is used to locate the existing emergency within the
        queue, as the internal lists are not sorted.

        Args:
            old_emergency_severity (int): The previous severity level of the
                emergency, used to determine which queue currently contains
                it.
            emergency (Emergency | EncryptedEmergency): The updated emergency
                instance to be re-queued.

        Raises:
            Exception: If the emergency to be updated cannot be found in the
                queue corresponding to the old severity level.
        """

        # NOTE: Linear Search is the best in this case because the lists are not
        # sorted.
        def linear_search(
            arr: list, new_emergency: Emergency | EncryptedEmergency
        ) -> int:
            index: int = 0
            for elem in arr:
                if (
                    (elem[2] is not None)
                    and (elem[2].user_uuid == new_emergency.user_uuid)
                    and (elem[2].emergency_id == new_emergency.emergency_id)
                ):
                    return index
                index += 1

            if index == len(arr):
                return -1

            return index

        if (old_emergency_severity >= 0) and (
            old_emergency_severity < self.min_medium_sev_score
        ):
            pos: int = linear_search(self.low_queue, emergency)
            if pos == -1:
                raise ValueError("Old emergency not found")

            self.low_queue.pop(pos)
        elif (old_emergency_severity >= self.min_medium_sev_score) and (
            old_emergency_severity < self.min_high_sev_score
        ):
            pos: int = linear_search(self.medium_queue, emergency)
            if pos == -1:
                raise ValueError("Old emergency not found")

            self.medium_queue.pop(pos)
        else:
            pos: int = linear_search(self.high_queue, emergency)
            if pos == -1:
                raise ValueError("Old emergency not found")

            self.high_queue.pop(pos)

        self.push_emergency(emergency)

import enum


class UserRole(enum.StrEnum):
    SENDER = "sender"
    DRIVER = "driver"
    RECIPIENT = "recipient"

class OrderStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"

class RouteStatusEnum(enum.Enum):
    ASSIGNED = "assigned"
    LOADED = "loaded"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    FAILED = "failed"

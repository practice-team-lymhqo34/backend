import enum


class UserRole(enum.StrEnum):
    CLIENT = "client"
    DRIVER = "driver"
    MANAGER = "manager"


class OrderStatus(enum.StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

import enum


class UserRole(enum.StrEnum):
    CLIENT = "client"
    DRIVER = "driver"
    MANAGER = "manager"

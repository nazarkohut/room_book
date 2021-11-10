from enum import Enum


class BreakfastEnum(int, Enum):
    not_included = 0
    included = 1
    paid = 2
    all_inclusive = 3


class TransportEnum(int, Enum):
    not_included = 0
    bus = 1
    car = 2


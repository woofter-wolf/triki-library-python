from dataclasses import dataclass


@dataclass(frozen=True)
class TRIKIDevice:
    name: str
    address: str

from dataclasses import dataclass, field
from typing import Any 

@dataclass(order=True)
class Event:
    time: int
    data: Any=field(compare=False)
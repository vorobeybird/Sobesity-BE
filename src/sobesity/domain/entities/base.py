from dataclasses import asdict, dataclass


@dataclass
class BaseEntity:
    def to_dict(self):
        return asdict(self)

class Unset:
    pass

unset = Unset()

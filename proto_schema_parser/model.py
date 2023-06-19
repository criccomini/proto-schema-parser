from dataclasses import dataclass, field
from enum import Enum


class FieldCardinality(str, Enum):
    REQUIRED = "REQUIRED"
    OPTIONAL = "OPTIONAL"
    REPEATED = "REPEATED"


@dataclass
class Option:
    name: str
    value: str


@dataclass
class Field:
    name: str
    type: str
    cardinality: FieldCardinality = FieldCardinality.REQUIRED
    options: list[Option] = field(default_factory=list)


@dataclass
class Message:
    name: str
    fields: list[Field] = field(default_factory=list)

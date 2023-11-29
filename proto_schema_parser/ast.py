from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum as PyEnum
from typing import Union


class FieldCardinality(str, PyEnum):
    REQUIRED = "REQUIRED"
    OPTIONAL = "OPTIONAL"
    REPEATED = "REPEATED"


# file: BYTE_ORDER_MARK? syntaxDecl? fileElement* EOF;
@dataclass
class File:
    syntax: str | None = None
    file_elements: list[FileElement] = field(default_factory=list)


# packageDecl: PACKAGE packageName SEMICOLON;
@dataclass
class Package:
    name: str


# importDecl: IMPORT ( WEAK | PUBLIC )? importedFileName SEMICOLON;
@dataclass
class Import:
    name: str
    weak: bool = False
    public: bool = False


# optionDecl: OPTION optionName EQUALS optionValue SEMICOLON;
@dataclass
class Option:
    name: str
    value: str


# messageDecl: MESSAGE messageName L_BRACE messageElement* R_BRACE;
@dataclass
class Message:
    name: str
    elements: list[MessageElement] = field(default_factory=list)


# messageFieldDecl: fieldDeclWithCardinality |
#                   messageFieldDeclTypeName fieldName EQUALS fieldNumber
#                        compactOptions? SEMICOLON;
@dataclass
class Field:
    name: str
    number: int
    type: str
    cardinality: FieldCardinality | None = None
    options: list[Option] = field(default_factory=list)


# mapFieldDecl: mapType fieldName EQUALS fieldNumber compactOptions? SEMICOLON;
# TODO Seems like the Buf .g4 grammar doesn't allow for cardinality on map fields?
@dataclass
class MapField:
    name: str
    number: int
    key_type: str
    value_type: str
    options: list[Option] = field(default_factory=list)


# groupDecl: fieldCardinality? GROUP fieldName EQUALS fieldNumber
#              compactOptions? L_BRACE messageElement* R_BRACE;
@dataclass
class Group:
    name: str
    number: int
    cardinality: FieldCardinality | None = None
    elements: list[MessageElement] = field(default_factory=list)


# oneofDecl: ONEOF oneofName L_BRACE oneofElement* R_BRACE;
@dataclass
class OneOf:
    name: str
    elements: list[OneOfElement] = field(default_factory=list)


# extensionRangeDecl: EXTENSIONS tagRanges compactOptions? SEMICOLON;
@dataclass
class ExtensionRange:
    ranges: list[str]
    options: list[Option] = field(default_factory=list)


# messageReservedDecl: RESERVED ( tagRanges | names ) SEMICOLON;
@dataclass
class Reserved:
    ranges: list[str] = field(default_factory=list)
    names: list[str] = field(default_factory=list)


# enumDecl: ENUM enumName L_BRACE enumElement* R_BRACE;
@dataclass
class Enum:
    name: str
    elements: list[EnumElement] = field(default_factory=list)


# enumValueDecl: enumValueName EQUALS enumValueNumber compactOptions? SEMICOLON;
@dataclass
class EnumValue:
    name: str
    number: int
    options: list[Option] = field(default_factory=list)


# enumReservedDecl: RESERVED ( enumValueRanges | names ) SEMICOLON;
@dataclass
class EnumReserved:
    ranges: list[str] = field(default_factory=list)
    names: list[str] = field(default_factory=list)


# extensionDecl: EXTEND extendedMessage L_BRACE extensionElement* R_BRACE;
@dataclass
class Extension:
    typeName: str
    elements: list[ExtensionElement] = field(default_factory=list)


# fileElement: importDecl |
#                packageDecl |
#                optionDecl |
#                messageDecl |
#                enumDecl |
#                extensionDecl |
#                serviceDecl |
#                emptyDecl;
FileElement = Union[Import, Package, Option, Message, Enum, Extension]

# messageElement: messageFieldDecl |
#                   groupDecl |
#                   oneofDecl |
#                   optionDecl |
#                   extensionRangeDecl |
#                   messageReservedDecl |
#                   messageDecl |
#                   enumDecl |
#                   extensionDecl |
#                   mapFieldDecl |
#                   emptyDecl;
MessageElement = Union[
    Field,
    Group,
    OneOf,
    Option,
    ExtensionRange,
    Reserved,
    Message,
    Enum,
    Extension,
    MapField,
]

# oneofElement: optionDecl |
#                 oneofFieldDecl |
#                 oneofGroupDecl;
OneOfElement = Union[Option, Field, Group]

# enumElement: optionDecl |
#                enumValueDecl |
#                enumReservedDecl |
#                emptyDecl;
EnumElement = Union[Option, EnumValue, EnumReserved]

# extensionElement: extensionFieldDecl |
#                     groupDecl;
ExtensionElement = Union[Field, Group]

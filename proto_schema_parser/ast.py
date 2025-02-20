from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum as PyEnum
from typing import List, Union


class FieldCardinality(str, PyEnum):
    REQUIRED = "REQUIRED"
    OPTIONAL = "OPTIONAL"
    REPEATED = "REPEATED"


# file: BYTE_ORDER_MARK? syntaxDecl? fileElement* EOF;
@dataclass
class File:
    """
    Represents a .proto file.

    Attributes:
        syntax: Union[str, None]
            The syntax level of the .proto file.
        file_elements: List[FileElement]
            A list of file elements in the .proto file.
    """

    syntax: Union[str, None] = None
    file_elements: List[FileElement] = field(default_factory=list)


# commentDecl: (LINE_COMMENT | BLOCK_COMMENT)
@dataclass
class Comment:
    """
    Represents a comment in a .proto file.

    Attributes:
        text: str
            The text of the comment.
    """

    text: str


# packageDecl: PACKAGE packageName SEMICOLON;
@dataclass
class Package:
    """
    Represents a package declaration in a .proto file.

    Attributes:
        name: str
            The name of the package.
    """

    name: str


# importDecl: IMPORT ( WEAK | PUBLIC )? importedFileName SEMICOLON;
@dataclass
class Import:
    """
    Represents an import declaration in a .proto file.

    Attributes:
        name: str
            The name of the imported file.
        weak: bool
            True if the import is weak, False otherwise.
        public: bool
            True if the import is public, False otherwise.
    """

    name: str
    weak: bool = False
    public: bool = False


@dataclass
class MessageLiteralField:
    """
    Represents a field in a message literal.

    Attributes:
        name: str
            The name of the field.
        value: MessageValue
            The value of the field.
    """

    name: str
    value: MessageValue


@dataclass
class MessageLiteral:
    """
    Represents a message literal.

    Attributes:
        fields: List[MessageLiteralField]
            The fields of the message literal.
    """

    fields: List[MessageLiteralField] = field(default_factory=list)


# optionDecl: OPTION optionName EQUALS optionValue SEMICOLON;
@dataclass
class Option:
    """
    Represents an option in a .proto file.

    Attributes:
        name: str
            The name of the option.
        value: Union[ScalarValue, MessageLiteral]
            The value of the option.
    """

    name: str
    value: Union[ScalarValue, MessageLiteral]


# messageDecl: MESSAGE messageName L_BRACE messageElement* R_BRACE;
@dataclass
class Message:
    """
    Represents a message in a .proto file.

    Attributes:
        name: str
            The name of the message.
        elements: List[MessageElement]
            The elements of the message.
    """

    name: str
    elements: List[MessageElement] = field(default_factory=list)


# messageFieldDecl: fieldDeclWithCardinality |
#                   messageFieldDeclTypeName fieldName EQUALS fieldNumber
#                        compactOptions? SEMICOLON;
@dataclass
class Field:
    """
    Represents a field in a message.

    Attributes:
        name: str
            The name of the field.
        number: int
            The number of the field.
        type: str
            The type of the field.
        cardinality: Union[FieldCardinality, None] = None
            The cardinality of the field.
        options: List[Option] = field(default_factory=list)
            The options of the field.
    """

    name: str
    number: int
    type: str
    cardinality: Union[FieldCardinality, None] = None
    options: List[Option] = field(default_factory=list)


# mapFieldDecl: mapType fieldName EQUALS fieldNumber compactOptions? SEMICOLON;
# TODO Seems like the Buf .g4 grammar doesn't allow for cardinality on map fields?
@dataclass
class MapField:
    """
    Represents a map field in a message.

    Attributes:
        name: str
            The name of the field.
        number: int
            The number of the field.
        key_type: str
            The type of the key.
        value_type: str
            The type of the value.
        options: List[Option] = field(default_factory=list)
            The options of the field.
    """

    name: str
    number: int
    key_type: str
    value_type: str
    options: List[Option] = field(default_factory=list)


# groupDecl: fieldCardinality? GROUP fieldName EQUALS fieldNumber
#              compactOptions? L_BRACE messageElement* R_BRACE;
@dataclass
class Group:
    """
    Represents a group in a message.

    Attributes:
        name: str
            The name of the group.
        number: int
            The number of the group.
        cardinality: Union[FieldCardinality, None] = None
            The cardinality of the group.
        elements: List[MessageElement] = field(default_factory=list)
            The elements of the group.
    """

    name: str
    number: int
    cardinality: Union[FieldCardinality, None] = None
    elements: List[MessageElement] = field(default_factory=list)


# oneofDecl: ONEOF oneofName L_BRACE oneofElement* R_BRACE;
@dataclass
class OneOf:
    """
    Represents an oneof in a message.

    Attributes:
        name: str
            The name of the oneof.
        elements: List[OneOfElement] = field(default_factory=list)
            The elements of the oneof.
    """

    name: str
    elements: List[OneOfElement] = field(default_factory=list)


# extensionRangeDecl: EXTENSIONS tagRanges compactOptions? SEMICOLON;
@dataclass
class ExtensionRange:
    """
    Represents an extension range in a message.

    Attributes:
        ranges: List[str]
            The ranges of the extension.
        options: List[Option] = field(default_factory=list)
            The options of the extension.
    """

    ranges: List[str]
    options: List[Option] = field(default_factory=list)


# messageReservedDecl: RESERVED ( tagRanges | names ) SEMICOLON;
@dataclass
class Reserved:
    """
    Represents a reserved range or name in a message.

    Attributes:
        ranges: List[str]
            The ranges of the reserved field.
        names: List[str]
            The names of the reserved field.
    """

    ranges: List[str] = field(default_factory=list)
    names: List[str] = field(default_factory=list)


# enumDecl: ENUM enumName L_BRACE enumElement* R_BRACE;
@dataclass
class Enum:
    """
    Represents an enum in a message.

    Attributes:
        name: str
            The name of the enum.
        elements: List[EnumElement] = field(default_factory=list)
            The elements of the enum.
    """

    name: str
    elements: List[EnumElement] = field(default_factory=list)


# enumValueDecl: enumValueName EQUALS enumValueNumber compactOptions? SEMICOLON;
@dataclass
class EnumValue:
    """
    Represents an enum value in an enum.

    Attributes:
        name: str
            The name of the enum value.
        number: int
            The number of the enum value.
        options: List[Option] = field(default_factory=list)
            The options of the enum value.
    """

    name: str
    number: int
    options: List[Option] = field(default_factory=list)


# enumReservedDecl: RESERVED ( enumValueRanges | names ) SEMICOLON;
@dataclass
class EnumReserved:
    """
    Represents a reserved range or name in an enum.

    Attributes:
        ranges: List[str]
            The ranges of the reserved field.
        names: List[str]
            The names of the reserved field.
    """

    ranges: List[str] = field(default_factory=list)
    names: List[str] = field(default_factory=list)


# extensionDecl: EXTEND extendedMessage L_BRACE extensionElement* R_BRACE;
@dataclass
class Extension:
    """
    Represents an extension in a message.

    Attributes:
        typeName: str
            The type name of the extension.
        elements: List[ExtensionElement] = field(default_factory=list)
            The elements of the extension.
    """

    typeName: str
    elements: List[ExtensionElement] = field(default_factory=list)


# serviceDecl: SERVICE serviceName L_BRACE serviceElement* R_BRACE;
@dataclass
class Service:
    """
    Represents a service in a message.

    Attributes:
        name: str
            The name of the service.
        elements: List[ServiceElement] = field(default_factory=list)
            The elements of the service.
    """

    name: str
    elements: List[ServiceElement] = field(default_factory=list)


# methodDecl: RPC methodName inputType RETURNS outputType SEMICOLON |
#             RPC methodName inputType RETURNS outputType L_BRACE methodElement* R_BRACE;
@dataclass
class Method:
    """
    Represents a method in a service.

    Attributes:
        name: str
            The name of the method.
        input_type: MessageType
            The input type of the method.
        output_type: MessageType
            The output type of the method.
        elements: List[MethodElement] = field(default_factory=list)
            The elements of the method.
    """

    name: str
    input_type: MessageType
    output_type: MessageType
    elements: List[MethodElement] = field(default_factory=list)


# messageType: L_PAREN STREAM? methodDeclTypeName R_PAREN;
@dataclass
class MessageType:
    """
    Represents a message type in a message.

    Attributes:
        type: str
            The type of the message.
        stream: bool = False
            Whether the message is a stream.
    """

    type: str
    stream: bool = False


# IDENTIFIER: LETTER ( LETTER | DECIMAL_DIGIT )*;
@dataclass
class Identifier:
    """
    Identifier is a simple dataclass to represent an unquoted identifier (such
    as an enumerator name). It's used as a value for scalar types that can't be
    parsed into a string, int, float, or bool.
    """

    name: str


# fileElement: importDecl |
#                packageDecl |
#                optionDecl |
#                messageDecl |
#                enumDecl |
#                extensionDecl |
#                serviceDecl |
#                commentDecl |
#                emptyDecl;
FileElement = Union[Import, Package, Option, Message, Enum, Extension, Service, Comment]
"""Represents a file element in a .proto file."""

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
#                   emptyDecl |
#                   commentDecl;
MessageElement = Union[
    Comment,
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
"""Represents a message element in a .proto file."""

# oneofElement: optionDecl |
#                 oneofFieldDecl |
#                 oneofGroupDecl |
#                 commentDecl;
OneOfElement = Union[Option, Field, Group, Comment]
"""Represents an oneof element in a .proto file."""

# enumElement: optionDecl |
#                enumValueDecl |
#                enumReservedDecl |
#                emptyDecl |
#                commentDecl;
EnumElement = Union[Option, EnumValue, EnumReserved, Comment]
"""Represents an enum element in a .proto file."""

# extensionElement: extensionFieldDecl |
#                     groupDecl;
ExtensionElement = Union[Field, Group, Comment]
"""Represents an extension element in a .proto file."""

# serviceElement: optionDecl |
#                   methodDecl |
#                   commentDecl |
#                   emptyDecl;
ServiceElement = Union[Option, Method, Comment]
"""Represents a service element in a .proto file."""

# methodElement: optionDecl |
#                 commentDecl |
#                 emptyDecl;
MethodElement = Union[Option, Comment]
"""Represents a method element in a .proto file."""

# Define a type alias for scalar values
ScalarValue = Union[str, int, float, bool, Identifier]
"""Represents a scalar value in a .proto file."""

# Define a recursive type alias for message values
MessageValue = Union[ScalarValue, MessageLiteral, List["MessageValue"]]
"""Represents a message value in a .proto file."""
